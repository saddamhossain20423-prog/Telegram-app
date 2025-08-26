from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import database
import models

# ডাটাবেস টেবিল তৈরি
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Telegram Mini App API")

# CORS সেটআপ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ডিপেন্ডেন্সি
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Telegram Mini App API is running"}

# রাউট ইম্পোর্ট
from routes import auth, wallet, referral, admin, tasks

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(wallet.router, prefix="/api/wallet", tags=["Wallet"])
app.include_router(referral.router, prefix="/api/referral", tags=["Referral"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)