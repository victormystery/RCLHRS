from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from schemas import UserCreate, UserOut, RoleOut, Token
from functions_crud import create_user, get_user_by_username
from auth.auth import authenticate_user, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["Users"])

# Define TokenWithUser to include user details in response
class TokenWithUser(Token):
    user: UserOut

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, user)

@router.post("/login", response_model=TokenWithUser)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=60)
    # Extract scopes from user roles or permissions
    scopes = []
    if hasattr(user, "role") and hasattr(user.role, "role_name"):
        scopes.append(user.role.role_name)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires, scopes=scopes
    )
    # Create UserOut instance for response
    user_out = UserOut(
        id=user.id,
        username=user.username,
        email=user.email,
        role=RoleOut(
            id=user.role.id,
            role_name=user.role.role_name,
            is_hr=user.role.is_hr,
            is_admin=user.role.is_admin
            
        )
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_out
    }