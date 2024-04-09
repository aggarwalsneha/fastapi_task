**Library Management System**  
This project is a simple yet powerful Library Management System built with FastAPI. It allows for creating, reading, updating, and deleting student records. Additionally, it supports filtering students based on criteria like country and age, demonstrating the powerful combination of FastAPI with MongoDB for building RESTful APIs.

**Features**  
Create Student Records: Add new student information including name, age, and address.
Read Student Records: Retrieve the details of students, with support for filtering by country and age.
Update Student Records: Modify existing student records.
Delete Student Records: Remove student records from the system.

**Prerequisites**  
Python 3.8 or higher
MongoDB

**Installation**  
1. Clone the repository:
git clone https://github.com/aggarwalsneha/fastapi_task.git
2. cd fastapi_task
3. Install the required Python packages:
pip install -r requirements.txt
4. Set up your MongoDB connection:
Edit the MONGODB_URL in your project files to match your MongoDB connection string.

**Running the Application**  
Run the FastAPI application with:
uvicorn app:app --reload
This command starts the server on http://127.0.0.1:8000. You can visit this URL in your web browser to see the automatically generated API documentation and test the API endpoints.

**API Endpoints**   
The system exposes several RESTful endpoints:  

POST /students: Create a new student record.  
GET /students: Retrieve a list of students, with optional filtering.  
PATCH /students/{student_id}: Update the details of an existing student.  
DELETE /students/{student_id}: Delete a student record.  
