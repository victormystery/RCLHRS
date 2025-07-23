from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from model import User
from database import get_db
from functions_crud import get_user_by_username
from schemas import TokenData
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env.custom")

# Security configurations
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 bearer token setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

#  Safe password verification
def verify_password(plain_password, hashed_password):
    if not hashed_password:
        return False
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"[Password Error] {e}")
        return False

# Hashing function
def get_password_hash(password):
    return pwd_context.hash(password)

#Secure user authentication
def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not user.password_hash:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

# Token creation
def create_access_token(
    data: dict, expires_delta: timedelta | None = None, scopes: list[str] = None
):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# User existence checker
def check_user_exists(db: Session, username: str) -> dict:
    user = get_user_by_username(db, username)
    if user:
        return {"detail": f"{username} already exists"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{username} not found",
    )