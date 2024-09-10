# app/schemas.py
from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings
class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department: str

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeInDBBase(EmployeeBase):
    id: int

    class Config:
        orm_mode = True

class Employee(EmployeeInDBBase):
    pass

class EmployeeInDB(EmployeeInDBBase):
    pass