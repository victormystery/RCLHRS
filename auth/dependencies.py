from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database import get_db
from model import User
from schemas import TokenData
from auth.auth import SECRET_KEY, ALGORITHM
from functions_crud import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


def require_hr(current_user: User = Depends(get_current_user)):
    if not current_user.role or not current_user.role.is_hr:
        raise HTTPException(status_code=403, detail="HR role required")
    return current_user


def require_admin(current_user: User = Depends(get_current_user)):
    if not current_user.role or not current_user.role.is_admin:
        raise HTTPException(status_code=403, detail="Admin role required")
    return current_user
