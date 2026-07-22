from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models, schemas
from database import SessionLocal
import bcrypt

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# For simplicity in this demo without python-jose, we will use a simple token strategy.
# A real implementation would use JWTs. Here we just return "token-{user_id}-{role}".

@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    new_user = models.User(
        full_name=user.full_name,
        username=user.username,
        password_hash=hashed_pw,
        approval_status="Pending"
    )
    db.add(new_user)
    
    # Audit log
    db.commit()
    db.refresh(new_user)
    
    log = models.SystemLog(user_id=new_user.id, action="REGISTER_USER", target_table="users", details="New signup pending approval")
    db.add(log)
    db.commit()
    
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not user or not bcrypt.checkpw(form_data.password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    if user.approval_status != "Approved":
        raise HTTPException(status_code=403, detail="Your account is pending Admin approval.")

    # Log the login
    log = models.SystemLog(user_id=user.id, action="LOGIN", target_table="users", target_id=user.id)
    db.add(log)
    
    # Simulate time tracking (add 15 mins for each activity/login session)
    if user.total_time_spent is None:
        user.total_time_spent = 0
    user.total_time_spent += 15
    
    db.commit()
    
    access_token = f"token-{user.id}-{user.role}"
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        _, user_id_str, role = token.split("-")
        user_id = int(user_id_str)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
    return user

def require_role(allowed_roles: list):
    def role_checker(current_user: models.User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return current_user
    return role_checker


# Trigger reload
