from pydantic import BaseModel, EmailStr
from typing import Optional
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
        orm_mode = True


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
        orm_mode = True


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

    class Config:
        orm_mode = True


# Bank Request schemas
class BankRequestBase(BaseModel):
    employee_id: int


class BankRequestCreate(BankRequestBase):
    pass


class BankRequestUpdate(BankRequestBase):
    pass


class BankRequestOut(BankRequestBase):
    id: int
    request_date: date
    status: Optional[str] = None
    details: Optional[str] = None

    class Config:
        orm_mode = True


# Home Office Request schemas
class HomeOfficeRequestBase(BaseModel):
    employee_id: int


class HomeOfficeRequestCreate(HomeOfficeRequestBase):
    pass


class HomeOfficeRequestUpdate(HomeOfficeRequestBase):
    pass


class HomeOfficeRequestOut(HomeOfficeRequestBase):
    id: int
    request_date: date
    status: Optional[str] = None
    details: Optional[str] = None

    class Config:
        orm_mode = True


# DBS Check schemas
class DBSCheckBase(BaseModel):
    employee_id: int


class DBSCheckCreate(DBSCheckBase):
    pass


class DBSCheckUpdate(DBSCheckBase):
    pass


class DBSCheckOut(DBSCheckBase):
    id: int
    check_date: date
    result: Optional[str] = None
    details: Optional[str] = None

    class Config:
        orm_mode = True


# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
