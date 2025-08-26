from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from datetime import datetime

router = APIRouter()

@router.get("/balance/{telegram_id}")
def get_balance(telegram_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"balance": user.balance}

@router.post("/deposit")
def deposit(telegram_id: str, amount: float, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # ব্যালেন্স আপডেট
    user.balance += amount
    
    # ট্রানজ্যাকশন রেকর্ড
    transaction = models.Transaction(
        user_id=user.id,
        amount=amount,
        type="deposit",
        status="completed"
    )
    db.add(transaction)
    db.commit()
    
    return {"success": True, "new_balance": user.balance}

@router.post("/withdraw")
def withdraw(telegram_id: str, amount: float, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    # ব্যালেন্স আপডেট
    user.balance -= amount
    
    # ট্রানজ্যাকশন রেকর্ড
    transaction = models.Transaction(
        user_id=user.id,
        amount=amount,
        type="withdraw",
        status="completed"
    )
    db.add(transaction)
    db.commit()
    
    return {"success": True, "new_balance": user.balance}