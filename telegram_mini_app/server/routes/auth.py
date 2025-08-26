from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.post("/login")
def login(telegram_id: str, username: str = None, first_name: str = "", last_name: str = "", db: Session = Depends(get_db)):
    # ইউজার খুঁজে দেখি
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    
    if not user:
        # নতুন ইউজার তৈরি করি
        user = models.User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return {
        "success": True,
        "user": {
            "id": user.id,
            "telegram_id": user.telegram_id,
            "username": user.username,
            "first_name": user.first_name,
            "balance": user.balance
        }
    }
