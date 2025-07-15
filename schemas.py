from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date


# Role schemas
class RoleBase(BaseModel):
    role_name: str
    is_hr: Optional[bool] = False
    is_admin: Optional[bool] = False


class RoleCreate(RoleBase):
    pass


class RoleOut(RoleBase):
    id: int

    class Config:
        from_attributes = True


# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role_id: int


class UserOut(UserBase):
    id: int
    role: RoleOut

    class Config:
        from_attributes = True


# Employee schemas
class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    date_of_birth: Optional[date] = None
    national_insurance_number: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    date_of_birth: Optional[date] = None
    national_insurance_number: Optional[str] = None


class EmployeeUpdate(EmployeeBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    national_insurance_number: Optional[str] = None


class EmployeeOut(EmployeeBase):
    id: int
    bank_request_statuses: Optional[List[str]] = None
    dbs_check_statuses: Optional[List[str]] = None
    home_office_request_statuses: Optional[List[str]] = None

    @staticmethod
    def from_orm_with_status(employee):
        # Extract statuses from bank requests, DBS checks, and home office requests
        bank_statuses = [
            req.status
            for req in getattr(employee, "bank_requests", [])
            if hasattr(req, "status") and req.status is not None
        ]
        dbs_statuses = [
            req.status
            for req in getattr(employee, "dbs_checks", [])
            if hasattr(req, "status") and req.status is not None
        ]
        home_office_statuses = [
            req.status
            for req in getattr(employee, "home_office_requests", [])
            if hasattr(req, "status") and req.status is not None
        ]

        # Validate and dump employee data
        data = EmployeeOut.model_validate(employee, from_attributes=True).model_dump()
        data["bank_request_statuses"] = bank_statuses
        data["dbs_check_statuses"] = dbs_statuses
        data["home_office_request_statuses"] = home_office_statuses
        return EmployeeOut(**data)

    class Config:
        from_attributes = True


# Bank Request schemas
class BankRequestBase(BaseModel):
    employee_id: int
    request_date: Optional[date] = None
    status: Optional[str] = None
    details: Optional[str] = None


class BankRequestCreate(BankRequestBase):
    employee_id: int
    request_date: Optional[date] = None
    status: Optional[str] = None
    details: Optional[str] = None


class BankRequestUpdate(BankRequestBase):
    employee_id: Optional[int] = None
    request_date: Optional[date] = None
    status: Optional[str] = None
    details: Optional[str] = None


class BankRequestOut(BankRequestBase):
    id: int

    class Config:
        from_attributes = True


# Home Office Request schemas
class HomeOfficeRequestBase(BaseModel):
    employee_id: int
    request_date: Optional[date] = None
    status: Optional[str] = None
    details: Optional[str] = None


class HomeOfficeRequestCreate(HomeOfficeRequestBase):
    employee_id: int


class HomeOfficeRequestUpdate(HomeOfficeRequestBase):
    pass


class HomeOfficeRequestOut(HomeOfficeRequestBase):
    id: int

    class Config:
        from_attributes = True


# DBS Check schemas
class DBSCheckBase(BaseModel):
    employee_id: int
    check_date: Optional[date] = None
    result: Optional[str] = None
    details: Optional[str] = None


class DBSCheckCreate(DBSCheckBase):
    employee_id: int


class DBSCheckUpdate(DBSCheckBase):
    pass


class DBSCheckOut(DBSCheckBase):
    id: int

    class Config:
        from_attributes = True


# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
