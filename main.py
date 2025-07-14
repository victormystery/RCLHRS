from fastapi import FastAPI
from database import engine, Base, SessionLocal
from routers import users, employees, bank_request, home_office, dbs
from model import Role, User
from auth.auth import get_password_hash

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

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
            "admin": {"is_admin": True, "is_hr": True},
            "hr": {"is_admin": False, "is_hr": True},
        }
        for role_name, flags in roles.items():
            r = db.query(Role).filter(Role.role_name == role_name).first()
            if not r:
                r = Role(
                    role_name=role_name,
                    is_admin=flags["is_admin"],
                    is_hr=flags["is_hr"],
                )
                db.add(r)
                db.commit()  # Commit after each add to avoid bulk insert issues

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
    finally:
        db.close()


init_db()
