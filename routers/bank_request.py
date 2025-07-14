from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from model import BankRequests
from schemas import BankRequestCreate, BankRequestUpdate, BankRequestOut
from auth.dependencies import get_current_user, require_hr, require_admin

router = APIRouter(prefix="/bank_requests", tags=["Bank Requests"])

@router.get("/", response_model=List[BankRequestOut])
def read_bank_requests(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(BankRequests).all()

@router.get("/{request_id}", response_model=BankRequestOut)
def read_bank_request(request_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    req = db.query(BankRequests).filter(BankRequests.id == request_id).first()
    if not req:
        raise HTTPException(404, "Bank request not found")
    return req

@router.post("/", response_model=BankRequestOut)
def create_bank_request(request: BankRequestCreate, db: Session = Depends(get_db), user=Depends(require_hr)):
    new_req = BankRequests(**request.dict())
    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    return new_req

@router.put("/{request_id}", response_model=BankRequestOut)
def update_bank_request(request_id: int, update_data: BankRequestUpdate, db: Session = Depends(get_db), user=Depends(require_hr)):
    req = db.query(BankRequests).filter(BankRequests.id == request_id).first()
    if not req:
        raise HTTPException(404, "Bank request not found")
    for key, val in update_data.dict(exclude_unset=True).items():
        setattr(req, key, val)
    db.commit()
    db.refresh(req)
    return req

@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bank_request(request_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    req = db.query(BankRequests).filter(BankRequests.id == request_id).first()
    if not req:
        raise HTTPException(404, "Bank request not found")
    db.delete(req)
    db.commit()
