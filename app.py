import os
from fastapi import FastAPI,status,Body,HTTPException,Response,Query
from pydantic import ConfigDict, BaseModel, Field,constr
from typing import Optional, List
from bson import ObjectId
from pymongo import ReturnDocument
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

MONGODB_URL=os.getenv('MONGODB_URL')

client=MongoClient(MONGODB_URL)
db = client.cosmos_task
student_collection = db.get_collection("student")
PyObjectId = Annotated[str, BeforeValidator(str)]

@app.get("/") 
def read_root(): 
    return {"message": "Hello World"}

class Address(BaseModel):
    city: str
    country: str

class StudentModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...,max_length=50,min_length=1)
    age: int = Field(gt=0)
    address: Address
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

class UpdateAddress(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None

class UpdateStudentModel(BaseModel):
    name: Optional[str] = Field(None,min_length=1)
    age: Optional[int] = Field(None, gt=0)
    address: Optional[UpdateAddress] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

class StudentDetail(BaseModel):
    name: str
    age: int

class StudentCollection(BaseModel):
    data: List[StudentDetail]

class NewStudentResponse(BaseModel):
    id: PyObjectId


@app.post(
    "/students/",
    response_description="Create Students",
    response_model=NewStudentResponse,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)

async def create_student(student: StudentModel = Body(...)):
    new_student = student_collection.insert_one(
        student.model_dump(by_alias=True, exclude=["id"])
    )
    created_student = student_collection.find_one(
        {"_id": new_student.inserted_id}
    )
    return {"id":created_student["_id"]}

@app.get(
    "/students/",
    response_description="List all students",
    response_model=StudentCollection,
    response_model_by_alias=False,
)
async def list_students(country: Optional[str] = None, age: Optional[int] = Query(None, ge=0)):
    query = {}
    if country:
        query["address.country"] = country
    if age is not None:
        query["age"] = {"$gte": age}
    students1 = list(student_collection.find(query))
    return StudentCollection(data=students1)


@app.get(
    "/students/{id}",
    response_description="Fetch student",
    response_model=StudentModel,
    response_model_by_alias=False,
)
async def show_student(id: str):

    if (
        student := student_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.patch(
    "/students/{id}",
    response_description="Update a student",
    response_model_by_alias=False,
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_student(id: str, data: UpdateStudentModel=Body(...)):
    data = data.model_dump(exclude_unset=True)
    if 'address' in data:
        for k,v in data['address'].items():
            data[f'address.{k}']=v
        data.pop('address')
    student = student_collection.find_one({"_id": ObjectId(id)})
    if len(student) >= 1:
        update_result = student_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return {}
        else:
            raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.delete(
    "/students/{id}",
    response_description="Delete a student"
)
async def delete_student(id: str):
    delete_result = student_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=404, detail=f"Student {id} not found")
