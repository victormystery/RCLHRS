from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from schemas import UserCreate, UserOut, Token
from functions_crud import create_user, get_user_by_username
from auth.auth import authenticate_user, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, user)


@router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=60)
    # Extract scopes from user roles or permissions
    scopes = []
    if hasattr(user, "role") and hasattr(user.role, "name"):
        # Example: use role name as scope
        scopes.append(user.role.name)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires, scopes=scopes
    )
    return {"access_token": access_token, "token_type": "bearer"}
