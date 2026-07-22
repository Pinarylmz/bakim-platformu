from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal
from routers.auth import require_role

router = APIRouter(prefix="/audit", tags=["audit"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.SystemLog])
def get_system_logs(
    skip: int = 0, limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["Admin", "Engineer"]))
):
    """Only Admins and Engineers can view the audit trail."""
    logs = db.query(models.SystemLog).order_by(models.SystemLog.timestamp.desc()).offset(skip).limit(limit).all()
    return logs

