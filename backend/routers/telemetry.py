from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import random

from database import get_db
import models, schemas

router = APIRouter(
    prefix="/telemetry",
    tags=["Telemetry Data"]
)

@router.post("/{uav_id}/simulate", response_model=schemas.TelemetryData)
def simulate_telemetry_for_uav(uav_id: int, db: Session = Depends(get_db)):
    """
    Simulates a new telemetry data point for a specific UAV.
    """
    uav = db.query(models.UAV).filter(models.UAV.id == uav_id, models.UAV.status != "Maintenance").first()
    if not uav:
        raise HTTPException(status_code=404, detail="İUAV not foundı veya bakımda")
    
    latest_telemetry = db.query(models.TelemetryData).filter(
        models.TelemetryData.uav_id == uav.id
    ).order_by(models.TelemetryData.timestamp.desc()).first()
    
    current_battery = 100.0
    if latest_telemetry and latest_telemetry.battery_level:
        current_battery = max(0.0, latest_telemetry.battery_level - random.uniform(0.5, 2.0))
        if current_battery == 0.0:
            current_battery = 100.0

    record = models.TelemetryData(
        uav_id=uav.id,
        timestamp=datetime.utcnow(),
        rpm_asymmetry=round(random.uniform(0.0, 5.0), 2),
        esc_temperature=round(random.uniform(60.0, 85.0), 1),
        vibration_level=round(random.uniform(0.5, 2.5), 2),
        battery_level=round(current_battery, 1)
    )
    db.add(record)
    
    # Update Hardware Parts Status for Testing
    parts = db.query(models.InstalledPart).filter(models.InstalledPart.uav_id == uav.id, models.InstalledPart.is_active == True).all()
    for part in parts:
        # Category 4 is Motor (affected by temperature)
        if part.category_id == 4:
            if record.esc_temperature > 75.0:
                part.status = "Critical"
            elif record.esc_temperature > 65.0:
                part.status = "Warning"
            else:
                part.status = "OK"
        # Category 1 is Main Rotor (affected by vibration)
        elif part.category_id == 1:
            if record.vibration_level > 1.8:
                part.status = "Critical"
            elif record.vibration_level > 1.2:
                part.status = "Warning"
            else:
                part.status = "OK"
                
    db.commit()
    db.refresh(record)
        
    return record

@router.get("/{uav_id}/latest", response_model=schemas.TelemetryData)
def get_latest_telemetry(uav_id: int, db: Session = Depends(get_db)):
    """
    Returns the most recent telemetry record for a specific UAV.
    """
    record = db.query(models.TelemetryData).filter(
        models.TelemetryData.uav_id == uav_id
    ).order_by(models.TelemetryData.timestamp.desc()).first()
    
    if not record:
        # Return default/empty data if none exists so frontend doesn't crash
        return schemas.TelemetryData(
            id=0,
            uav_id=uav_id,
            timestamp=datetime.utcnow(),
            rpm_asymmetry=0.0,
            esc_temperature=20.0, # Ambient temp
            vibration_level=0.0,
            battery_level=100.0
        )
        
    return record

