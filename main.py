from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
from routers import users, employees, bank_request, home_office, dbs
from model import Role, User
from auth.auth import get_password_hash

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (all CRUD and auth logic should be in routers)
app.include_router(users.router)
app.include_router(employees.router)
app.include_router(bank_request.router)
app.include_router(home_office.router)
app.include_router(dbs.router)


# Initial DB setup for roles and admin user
def init_db():
    db = SessionLocal()
    try:
        # Create roles if not exist
        roles = {
            "admin": {"is_admin": True, "is_hr": True, "is_employee": True},
            "hr": {"is_admin": False, "is_hr": True, "is_employee": True},
            "employee": {"is_admin": False, "is_hr": False, "is_employee": True},
        }
        for role_name, flags in roles.items():
            r = db.query(Role).filter(Role.role_name == role_name).first()
            if not r:
                r = Role(
                    role_name=role_name,
                    is_admin=flags["is_admin"],
                    is_hr=flags["is_hr"],
                    is_employee=flags["is_employee"],
                )
                db.add(r)
                db.commit()  # Commit after each add

        # Create default admin user if not exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_role = db.query(Role).filter(Role.role_name == "admin").first()
            user = User(
                username="admin",
                email="admin@gmail.com",
                password_hash=get_password_hash("adminpassword"),
                role_id=admin_role.id,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            # Create matching employee entry
            from model import Employee

            employee = Employee(
                user_id=user.id,
                first_name="Admin",
                last_name="User",
                email=user.email,
                phone_number="0000000000",
                department="Administration",
                position="System Administrator",
            )
            db.add(employee)
            db.commit()

    finally:
        db.close()


init_db()
