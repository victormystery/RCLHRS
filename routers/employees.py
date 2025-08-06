from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from model import Employee
from schemas import EmployeeCreate, EmployeeUpdate, EmployeeOut
from auth.dependencies import get_current_user, require_hr, require_admin

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/", response_model=List[EmployeeOut])
def read_employees(db: Session = Depends(get_db), user=Depends(get_current_user)):
    employees = (
        db.query(Employee)
        .options(
            joinedload(Employee.bank_requests),
            joinedload(Employee.dbs_checks),
            joinedload(Employee.home_office_requests),
        )
        .all()
    )
    return [EmployeeOut.from_orm_with_status(emp) for emp in employees]


@router.get("/{employee_id}", response_model=EmployeeOut)
def read_employee(
    employee_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    employee = (
        db.query(Employee)
        .options(
            joinedload(Employee.bank_requests),
            joinedload(Employee.dbs_checks),
            joinedload(Employee.home_office_requests),
        )
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(404, "Employee not found")

    return EmployeeOut.from_orm_with_status(employee)


@router.post("/", response_model=EmployeeOut)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = Employee(**employee.model_dump())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return EmployeeOut.from_orm_with_status(new_employee)


@router.put("/{employee_id}", response_model=EmployeeOut)
def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_hr),
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(404, "Employee not found")

    for key, val in employee_update.dict(exclude_unset=True).items():
        setattr(employee, key, val)

    db.commit()
    db.refresh(employee)
    return EmployeeOut.from_orm_with_status(employee)


@router.delete("/{employee_id}", response_model=str)
def delete_employee(
    employee_id: int, db: Session = Depends(get_db), user=Depends(require_admin)
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(404, "Employee not found")

    db.delete(employee)
    db.commit()
    return "Successfully deleted employee"
