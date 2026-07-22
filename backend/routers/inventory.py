from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal
from routers.auth import require_role, get_current_user

router = APIRouter(prefix="/inventory", tags=["inventory"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/categories", response_model=List[schemas.PartCategory])
def read_categories(db: Session = Depends(get_db)):
    return db.query(models.PartCategory).filter(models.PartCategory.is_active == True).all()

@router.get("/installed-parts", response_model=List[schemas.InstalledPart])
def read_all_installed_parts(db: Session = Depends(get_db)):
    return db.query(models.InstalledPart).filter(models.InstalledPart.is_active == True).all()

@router.get("/installed-parts/{uav_id}", response_model=List[schemas.InstalledPart])
def read_installed_parts(uav_id: int, db: Session = Depends(get_db)):
    return db.query(models.InstalledPart).filter(models.InstalledPart.uav_id == uav_id, models.InstalledPart.is_active == True).all()

@router.post("/installed-parts", response_model=schemas.InstalledPart)
def install_part(
    part: schemas.InstalledPartCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["Technician", "Engineer", "Admin"]))
):
    import uuid
    
    # Auto-generate or suffix serial number to prevent duplicate errors
    if not part.serial_number or part.serial_number.strip() == "":
        part.serial_number = f"AUTO-{uuid.uuid4().hex[:8].upper()}"
    else:
        existing = db.query(models.InstalledPart).filter(models.InstalledPart.serial_number == part.serial_number).first()
        if existing:
            part.serial_number = f"{part.serial_number}-{uuid.uuid4().hex[:4].upper()}"

    uav = db.query(models.UAV).filter(models.UAV.id == part.uav_id).first()
    if not uav:
        raise HTTPException(status_code=404, detail="UAV not found")
        
    db_part = models.InstalledPart(**part.model_dump())
    db.add(db_part)
    
    log = models.SystemLog(user_id=current_user.id, action="INSTALL_PART", target_table="installed_parts", details=f"Installed {part.serial_number} on {uav.serial_number}")
    db.add(log)
    
    db.commit()
    db.refresh(db_part)
    return db_part

@router.delete("/installed-parts/{part_id}")
def uninstall_part(
    part_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["Technician", "Engineer", "Admin"]))
):
    """Soft delete uninstalled parts"""
    part = db.query(models.InstalledPart).filter(models.InstalledPart.id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
        
    part.is_active = False
    
    log = models.SystemLog(user_id=current_user.id, action="UNINSTALL_PART", target_table="installed_parts", target_id=part.id)
    db.add(log)
    
    db.commit()
    return {"message": "Part uninstalled successfully."}
