import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

import models, schemas, crud

app = FastAPI()

# Create tables on startup
@app.on_event("startup")
def startup_event():
    try:
        models.Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Warning: Could not create tables on startup: {e}")

# Allow both localhost and deployed frontend URL
allowed_origins = [
    "http://localhost:4200",
    "https://ehrmsui.onrender.com",
    os.getenv("FRONTEND_URL", "http://localhost:4200")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create_employee")
def add_employee(emp: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, emp)

@app.get("/get_employee/{employee_id}")
def get_employee(employee_id: str, db: Session = Depends(get_db)):
    return crud.get_employee(db, employee_id)

@app.get("/get_employees")
def list_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)

@app.delete("/employees/{employee_id}")
def remove_employee(employee_id: str, db: Session = Depends(get_db)):
    return crud.delete_employee(db, employee_id)

@app.post("/mark_attendance")
def add_attendance(att: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    return crud.mark_attendance(db, att)

@app.get("/get_attendance/{employee_id}")
def view_attendance(employee_id: str, db: Session = Depends(get_db)):
    return crud.get_attendance(db, employee_id)

@app.get("/get_all_attendance")
def view_all_attendance(db: Session = Depends(get_db)):
    return crud.get_all_attendance(db)
