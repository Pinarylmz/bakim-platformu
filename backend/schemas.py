from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    full_name: Optional[str] = None
    username: str
    role: Optional[str] = None

class UserRegister(BaseModel):
    full_name: str
    username: str
    password: str

class UserCreate(UserBase):
    password: str

class UserApprove(BaseModel):
    role: str
    approval_status: str

class ProfileUpdate(BaseModel):
    full_name: str

class User(UserBase):
    id: int
    is_active: bool
    approval_status: str
    created_at: datetime
    total_time_spent: int = 0
    class Config:
        from_attributes = True

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class SystemLogBase(BaseModel):
    action: str
    target_table: str
    target_id: Optional[int] = None
    details: Optional[str] = None

class SystemLog(SystemLogBase):
    id: int
    user_id: Optional[int]
    timestamp: datetime
    class Config:
        from_attributes = True

class PartCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class PartCategory(PartCategoryBase):
    id: int
    is_active: bool
    class Config:
        from_attributes = True

class InstalledPartBase(BaseModel):
    category_id: int
    serial_number: Optional[str] = None
    name: str
    max_flight_hours: float
    max_cycles: Optional[int] = None

class InstalledPartCreate(InstalledPartBase):
    uav_id: int

class InstalledPart(InstalledPartBase):
    id: int
    uav_id: int
    installation_date: datetime
    current_flight_hours: float
    current_cycles: int
    status: str
    is_active: bool
    category: Optional[PartCategory] = None
    class Config:
        from_attributes = True

class UAVBase(BaseModel):
    serial_number: str
    model_name: str
    total_flight_hours: float = 0.0
    total_flight_cycles: int = 0
    status: str = "Flight Ready"

class UAVCreate(UAVBase):
    pass

class UAV(UAVBase):
    id: int
    is_active: bool
    parts: List[InstalledPart] = []
    class Config:
        from_attributes = True

class WorkOrderBase(BaseModel):
    part_id: Optional[int] = None
    severity: int
    description: str

class WorkOrderCreate(WorkOrderBase):
    uav_id: int

class WorkOrder(WorkOrderBase):
    id: int
    uav_id: int
    action_taken: Optional[str] = None
    technician_id: int
    engineer_id: Optional[int] = None
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class WorkOrderApprove(BaseModel):
    action_taken: str

class PreFlightChecklistBase(BaseModel):
    checklist_data: Dict[str, Any]
    is_passed: bool

class PreFlightChecklistCreate(PreFlightChecklistBase):
    uav_id: int

class PreFlightChecklist(PreFlightChecklistBase):
    id: int
    uav_id: int
    technician_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class TelemetryDataBase(BaseModel):
    rpm_asymmetry: Optional[float] = None
    esc_temperature: Optional[float] = None
    vibration_level: Optional[float] = None
    battery_level: Optional[float] = None

class TelemetryDataCreate(TelemetryDataBase):
    uav_id: int

class TelemetryData(TelemetryDataBase):
    id: int
    uav_id: int
    timestamp: datetime
    class Config:
        from_attributes = True
