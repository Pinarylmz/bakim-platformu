from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal
from routers.auth import require_role

router = APIRouter(prefix="/work-orders", tags=["work_orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.WorkOrder])
def get_work_orders(db: Session = Depends(get_db)):
    return db.query(models.WorkOrder).filter(models.WorkOrder.is_active == True).all()

@router.post("/", response_model=schemas.WorkOrder)
def create_work_order(
    wo: schemas.WorkOrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["Technician", "Engineer", "Admin"]))
):
    """Maker: Technician reports damage/squawk"""
    uav = db.query(models.UAV).filter(models.UAV.id == wo.uav_id).first()
    if not uav:
        raise HTTPException(status_code=404, detail="İUAV not foundı")
        
    uav.status = "Pending Review" # Airworthiness lock
    
    new_wo = models.WorkOrder(
        **wo.model_dump(),
        technician_id=current_user.id,
        status="Pending Review"
    )
    db.add(new_wo)
    
    log = models.SystemLog(user_id=current_user.id, action="CREATE_WORK_ORDER", target_table="work_orders")
    db.add(log)
    
    db.commit()
    db.refresh(new_wo)
    return new_wo

@router.put("/{wo_id}/approve", response_model=schemas.WorkOrder)
def approve_work_order(
    wo_id: int,
    approval: schemas.WorkOrderApprove,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["Engineer", "Admin"]))
):
    """Checker: Engineer reviews and approves work"""
    wo = db.query(models.WorkOrder).filter(models.WorkOrder.id == wo_id).first()
    if not wo:
        raise HTTPException(status_code=404, detail="İş EWork Order not foundı")
        
    if wo.status == "Closed":
        raise HTTPException(status_code=400, detail="Work Order already closed")
        
    wo.status = "Closed"
    wo.engineer_id = current_user.id
    wo.action_taken = approval.action_taken
    
    # Check if UAV has any other pending work orders
    pending_wos = db.query(models.WorkOrder).filter(
        models.WorkOrder.uav_id == wo.uav_id, 
        models.WorkOrder.status != "Closed",
        models.WorkOrder.id != wo.id
    ).count()
    
    if pending_wos == 0:
        uav = db.query(models.UAV).filter(models.UAV.id == wo.uav_id).first()
        uav.status = "Flight Ready" # Unlock Airworthiness
        
    log = models.SystemLog(user_id=current_user.id, action="APPROVE_WORK_ORDER", target_table="work_orders", target_id=wo.id)
    db.add(log)
    
    db.commit()
    db.refresh(wo)
    return wo

