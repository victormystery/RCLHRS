from sqlalchemy.orm import Session
from model import User, Role, Employee, BankRequests, HomeOfficeRequests, DBSChecks
from schemas import (
    UserCreate,
    EmployeeCreate,
    BankRequestCreate,
    HomeOfficeRequestCreate,
    DBSCheckCreate,
)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# User
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    # Hash the password
    hashed_password = pwd_context.hash(user.password)

    # Create and add the user
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role_id=user.role_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Get the role
    role = db.query(Role).filter(Role.id == user.role_id).first()

    # If the role includes employee privileges, create an Employee record
    if role and role.is_employee:
        db_employee = Employee(
            user_id=db_user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number,
            department=user.department,
            position=user.position,
            date_of_birth=user.date_of_birth,
            national_insurance_number=user.national_insurance_number,
        )
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)

    return db_user


# Employee
def create_employee(db: Session, employee: EmployeeCreate):
    db_emp = Employee(**employee.model_dump())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp


# BankRequests
def create_bank_request(db: Session, request: BankRequestCreate):
    db_req = BankRequests(**request.model_dump())
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return db_req


# HomeOfficeRequests
def create_home_office_request(db: Session, request: HomeOfficeRequestCreate):
    db_req = HomeOfficeRequests(**request.model_dump())
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return db_req


# DBSChecks
def create_dbs_check(db: Session, check: DBSCheckCreate):
    db_check = DBSChecks(**check.model_dump())
    db.add(db_check)
    db.commit()
    db.refresh(db_check)
    return db_check
