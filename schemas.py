from datetime import date
from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    employee_id: str
    full_name: str
    email: str
    department: str

class AttendanceCreate(BaseModel):
    employee_id: str
    date: date
    status: str
