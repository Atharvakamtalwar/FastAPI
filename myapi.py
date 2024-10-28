from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1 : {
        "Name" : "Atharva",
        "Roll" : 32
    },
    2 : {
        "Name" : "Sushant",
        "Roll" : 28
    }
}

class Student(BaseModel):
    Name: str
    Roll: int

class UpdateStudent(BaseModel):
    Name: Optional[str] = None
    Roll: Optional[int] = None

@app.get("/")
def index():
    return {"Name" : "Atharva Kamtalwar"}

@app.get("/get-student/{student_id}")
def get_student(student_id :int = Path(..., description="Student ID", gt=0, lt=10)):
    return students[student_id]

@app.get("/get-student-by-name/{student_id}")
def get_student(*, student_id:int, name:Optional[str] = None, test : Optional[int] = None):
    for id in students:
        if students[id]["Name"] == name:
            return students[id]
    return {"Data": "Not Found"}

@app.post("/create-student/{student_id}")
def create_student(student_id:int, student: Student):
    if student_id in students:
        return {"Error": "Student Exists"}
    students[student_id] = student
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id:int, student:UpdateStudent):
    if student_id not in students:
        return {"Error":"Student doesn't exist"}
    
    # students[student_id] = student

    if student.Name != None:
        students[student_id]["Name"] = student.Name

    if student.Roll != None:
        students[student_id]["Roll"] = student.Roll

    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error":"Student doesn't exists"}

    del students[student_id]
    return {"Message": "Student deleted successfully"}