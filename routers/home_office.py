from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from model import HomeOfficeRequests
from schemas import (
    HomeOfficeRequestCreate,
    HomeOfficeRequestUpdate,
    HomeOfficeRequestOut,
)
from auth.dependencies import get_current_user, require_hr, require_admin

router = APIRouter(prefix="/home_office_requests", tags=["Home Office Requests"])


@router.get("/", response_model=List[HomeOfficeRequestOut])
def read_home_office_requests(
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return db.query(HomeOfficeRequestOut).all()


@router.get("/{request_id}", response_model=HomeOfficeRequestOut)
def read_home_office_request(
    request_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    req = (
        db.query(HomeOfficeRequestOut)
        .filter(HomeOfficeRequestOut.id == request_id)
        .first()
    )
    if not req:
        raise HTTPException(404, "Home Office request not found")
    return req


@router.post("/", response_model=HomeOfficeRequestOut)
def create_home_office_request(
    request: HomeOfficeRequestCreate,
    db: Session = Depends(get_db),
    user=Depends(require_hr),
):
    new_req = HomeOfficeRequests(**request.dict())
    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    return new_req


@router.put("/{request_id}", response_model=HomeOfficeRequestOut)
def update_home_office_request(
    request_id: int,
    update_data: HomeOfficeRequestUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_hr),
):
    req = (
        db.query(HomeOfficeRequests).filter(HomeOfficeRequests.id == request_id).first()
    )
    if not req:
        raise HTTPException(404, "Home Office request not found")
    for key, val in update_data.dict(exclude_unset=True).items():
        setattr(req, key, val)
    db.commit()
    db.refresh(req)
    return req


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_home_office_request(
    request_id: int, db: Session = Depends(get_db), user=Depends(require_admin)
):
    req = (
        db.query(HomeOfficeRequests).filter(HomeOfficeRequests.id == request_id).first()
    )
    if not req:
        raise HTTPException(404, "Home Office request not found")
    db.delete(req)
    db.commit()
