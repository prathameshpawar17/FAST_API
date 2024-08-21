from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, Employee as EmployeeSchema

router = APIRouter()

@router.post("/employees", response_model=EmployeeSchema)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/employees", response_model=List[EmployeeSchema])
def read_employees(skip: int = 0, limit: int = 2, db: Session = Depends(get_db)):
    employees = db.query(Employee).offset(skip).limit(limit).all()
    return employees