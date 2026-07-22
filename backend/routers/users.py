from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal
from routers.auth import get_current_user, require_role
import hashlib
import bcrypt

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    # A simple SHA-256 hash for demonstration instead of storing plain text.
    # Note: In a real system we would use passlib with bcrypt.
    return hashlib.sha256(password.encode()).hexdigest()

# ----------------- ADMIN USER MANAGEMENT -----------------

@router.get("/", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["Admin"]))):
    return db.query(models.User).filter(models.User.is_active == True, models.User.approval_status == "Approved").all()

@router.get("/pending", response_model=List[schemas.User])
def get_pending_users(db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["Admin"]))):
    return db.query(models.User).filter(models.User.is_active == True, models.User.approval_status == "Pending").all()

@router.get("/tracking", response_model=List[schemas.User])
def get_user_tracking(db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["Admin"]))):
    return db.query(models.User).filter(models.User.is_active == True).all()

@router.put("/{user_id}/approve")
def approve_user(user_id: int, approval: schemas.UserApprove, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["Admin"]))):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.approval_status = approval.approval_status
    if approval.approval_status == "Approved":
        user.role = approval.role
        
    log = models.SystemLog(user_id=current_user.id, action="APPROVE_USER", target_table="users", target_id=user.id, details=f"Status: {approval.approval_status}, Role: {approval.role}")
    db.add(log)
    db.commit()
    return {"message": f"User {approval.approval_status} successfully"}

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["Admin"]))):
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    db_user = models.User(
        username=user.username,
        role=user.role,
        password_hash=hashed_pw
    )
    db.add(db_user)
    
    log = models.SystemLog(user_id=current_user.id, action="CREATE_USER", target_table="users", details=f"Created {user.username}")
    db.add(log)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(["Admin"]))):
    """Soft Delete User"""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
        
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user.username == 'admin':
        raise HTTPException(status_code=403, detail="Cannot delete the main admin account")
        
    user.is_active = False
    
    log = models.SystemLog(user_id=current_user.id, action="DELETE_USER", target_table="users", target_id=user.id)
    db.add(log)
    
    db.commit()
    return {"message": "User deleted successfully"}

# ----------------- USER PROFILE (ALL ROLES) -----------------

@router.get("/me", response_model=schemas.User)
def get_my_profile(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.get("/me/activities")
def get_my_activities(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    logs = db.query(models.SystemLog).filter(
        models.SystemLog.user_id == current_user.id
    ).order_by(models.SystemLog.timestamp.desc()).limit(15).all()
    
    return logs

@router.put("/me/profile", response_model=schemas.User)
def update_profile(payload: schemas.ProfileUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    current_user.full_name = payload.full_name
    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/me/password")
def change_password(payload: schemas.PasswordChange, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Since we use plain text in this mockup (due to seed.py):
    if current_user.password_hash != payload.current_password:
        raise HTTPException(status_code=400, detail="Incorrect current password")
        
    current_user.password_hash = payload.new_password
    
    log = models.SystemLog(user_id=current_user.id, action="CHANGE_PASSWORD", target_table="users", target_id=current_user.id)
    db.add(log)
    
    db.commit()
    return {"message": "Password updated successfully"}

