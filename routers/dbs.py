from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from model import DBSChecks
from schemas import DBSCheckCreate, DBSCheckUpdate, DBSCheckOut
from auth.dependencies import get_current_user, require_hr, require_admin

router = APIRouter(prefix="/dbs_checks", tags=["DBS Checks"])

@router.get("/", response_model=List[DBSCheckOut])
def read_dbs_checks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(DBSChecks).all()

@router.get("/{check_id}", response_model=DBSCheckOut)
def read_dbs_check(check_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    check = db.query(DBSChecks).filter(DBSChecks.id == check_id).first()
    if not check:
        raise HTTPException(404, "DBS check not found")
    return check

@router.post("/", response_model=DBSCheckOut)
def create_dbs_check(check: DBSCheckCreate, db: Session = Depends(get_db), user=Depends(require_hr)):
    new_check = DBSChecks(**check.dict())
    db.add(new_check)
    db.commit()
    db.refresh(new_check)
    return new_check

@router.put("/{check_id}", response_model=DBSCheckOut)
def update_dbs_check(check_id: int, update_data: DBSCheckUpdate, db: Session = Depends(get_db), user=Depends(require_hr)):
    check = db.query(DBSChecks).filter(DBSChecks.id == check_id).first()
    if not check:
        raise HTTPException(404, "DBS check not found")
    for key, val in update_data.dict(exclude_unset=True).items():
        setattr(check, key, val)
    db.commit()
    db.refresh(check)
    return check

@router.delete("/{check_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dbs_check(check_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    check = db.query(DBSChecks).filter(DBSChecks.id == check_id).first()
    if not check:
        raise HTTPException(404, "DBS check not found")
    db.delete(check)
    db.commit()
