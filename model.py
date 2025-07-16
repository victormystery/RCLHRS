from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, nullable=False)
    is_hr = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_employee = Column(Boolean, default=False)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="users")
    employee = relationship("Employee", back_populates="user", uselist=False)


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    department = Column(String, nullable=True)
    position = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    national_insurance_number = Column(String, nullable=True)

    bank_requests = relationship("BankRequests", back_populates="employee")
    dbs_checks = relationship("DBSChecks", back_populates="employee")
    home_office_requests = relationship("HomeOfficeRequests", back_populates="employee")
    user = relationship("User", back_populates="employee")


class BankRequests(Base):
    __tablename__ = "bank_requests"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    request_date = Column(Date, nullable=True)
    status = Column(String, nullable=True)
    details = Column(String, nullable=True)

    employee = relationship("Employee", back_populates="bank_requests")


class HomeOfficeRequests(Base):
    __tablename__ = "home_office_requests"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    request_date = Column(Date, nullable=True)
    status = Column(String, nullable=True)
    details = Column(String, nullable=True)

    employee = relationship("Employee", back_populates="home_office_requests")


class DBSChecks(Base):
    __tablename__ = "dbs_checks"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    request_date = Column(Date, nullable=True)
    status = Column(String, nullable=True)
    details = Column(String, nullable=True)

    employee = relationship("Employee", back_populates="dbs_checks")
