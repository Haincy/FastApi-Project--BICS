from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import ARUser
from app.schemas.user_schema import ARUserCreate, ARUserOut
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=ARUserOut)
def create_user(user: ARUserCreate, db: Session = Depends(get_db)):
    db_user = ARUser(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=list[ARUserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(ARUser).all()
