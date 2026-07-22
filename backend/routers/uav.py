from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal
from routers.auth import get_current_user, require_role

router = APIRouter(prefix="/uavs", tags=["uavs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.UAV])
def read_uavs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.UAV).filter(models.UAV.is_active == True).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.UAV)
def create_uav(
    uav: schemas.UAVCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["Engineer", "Admin"]))
):
    existing = db.query(models.UAV).filter(models.UAV.serial_number == uav.serial_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="A UAV with this Serial Number/QR already exists.")
        
    db_uav = models.UAV(**uav.model_dump())
    db.add(db_uav)
    
    log = models.SystemLog(user_id=current_user.id, action="CREATE_UAV", target_table="uavs", details=f"Added UAV {uav.serial_number}")
    db.add(log)
    
    db.commit()
    db.refresh(db_uav)
    return db_uav

@router.get("/{serial_number}")
def read_uav_profile(serial_number: str, db: Session = Depends(get_db)):
    uav = db.query(models.UAV).filter(models.UAV.serial_number == serial_number, models.UAV.is_active == True).first()
    if not uav:
        raise HTTPException(status_code=404, detail="İUAV not foundı")
    
    parts = db.query(models.InstalledPart).filter(models.InstalledPart.uav_id == uav.id, models.InstalledPart.is_active == True).all()
    work_orders = db.query(models.WorkOrder).filter(models.WorkOrder.uav_id == uav.id).order_by(models.WorkOrder.created_at.desc()).all()
    
    return {
        "uav": uav,
        "installed_parts": parts,
        "work_orders": work_orders
    }

@router.post("/{uav_id}/checklist", response_model=schemas.PreFlightChecklist)
def submit_checklist(
    uav_id: int, 
    checklist: schemas.PreFlightChecklistCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["Technician", "Engineer", "Admin"]))
):
    uav = db.query(models.UAV).filter(models.UAV.id == uav_id).first()
    if not uav or uav.status != "Flight Ready":
        raise HTTPException(status_code=400, detail="İHA Flight Ready değil. Lütfen önce bekleyen iş emirlerini kapatın.")
        
    new_cl = models.PreFlightChecklist(
        uav_id=uav_id,
        technician_id=current_user.id,
        checklist_data=checklist.checklist_data,
        is_passed=checklist.is_passed
    )
    db.add(new_cl)
    
    log = models.SystemLog(user_id=current_user.id, action="SUBMIT_CHECKLIST", target_table="pre_flight_checklists", details=f"Passed: {checklist.is_passed}")
    db.add(log)
    
    db.commit()
    db.refresh(new_cl)
    return new_cl

@router.post("/{uav_id}/telemetry/upload-ulog")
async def upload_telemetry(
    uav_id: int, 
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["Engineer", "Admin"]))
):
    """Parses PX4 .ulog files (Simulated) and generates trend analysis"""
    uav = db.query(models.UAV).filter(models.UAV.id == uav_id).first()
    if not uav:
        raise HTTPException(status_code=404, detail="İUAV not foundı")
        
    # Simulate parsing the .ulog file for anomalies
    rpm_asymmetry = 5.2 # %
    esc_temp = 85.0 # Celsius
    vibration = 1.2 # G
    
    telemetry = models.TelemetryData(
        uav_id=uav.id, rpm_asymmetry=rpm_asymmetry, esc_temperature=esc_temp, vibration_level=vibration
    )
    db.add(telemetry)
    
    # Kestirimci BakÄ±m / Predictive Maintenance Logic
    if esc_temp > 80.0 or rpm_asymmetry > 5.0:
        uav.status = "Pending Review" # Automatically ground the UAV
        wo = models.WorkOrder(
            uav_id=uav.id, severity=2, description="Predictive Maintenance Alert: High ESC Temp or RPM Asymmetry detected in latest ulog.",
            technician_id=current_user.id, status="Open"
        )
        db.add(wo)
        
        log = models.SystemLog(user_id=current_user.id, action="PREDICTIVE_ALERT", target_table="uavs", target_id=uav.id)
        db.add(log)
        
    db.commit()
    return {"message": "Telemetry processed. Alerts generated if thresholds exceeded."}

