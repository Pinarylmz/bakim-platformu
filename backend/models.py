from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class BaseModel(Base):
    __abstract__ = True
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, nullable=True)  # Admin, Engineer, Technician
    approval_status = Column(String, default="Pending") # Pending, Approved, Rejected
    total_time_spent = Column(Integer, default=0) # Time spent in minutes
    
    system_logs = relationship("SystemLog", back_populates="user")
    work_orders_created = relationship("WorkOrder", foreign_keys="[WorkOrder.technician_id]", back_populates="technician")
    work_orders_approved = relationship("WorkOrder", foreign_keys="[WorkOrder.engineer_id]", back_populates="engineer")
    checklists = relationship("PreFlightChecklist", back_populates="technician")

class SystemLog(BaseModel):
    __tablename__ = "system_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String)
    target_table = Column(String)
    target_id = Column(Integer, nullable=True)
    details = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="system_logs")

class UAV(BaseModel):
    __tablename__ = "uavs"
    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, unique=True, index=True)  # Used for QR scanning
    model_name = Column(String, index=True)
    total_flight_hours = Column(Float, default=0.0)
    total_flight_cycles = Column(Integer, default=0)
    # Statuses: Flight Ready, Pending Review, Maintenance, AOG
    status = Column(String, default="Flight Ready")
    
    parts = relationship("InstalledPart", back_populates="uav")
    work_orders = relationship("WorkOrder", back_populates="uav")
    checklists = relationship("PreFlightChecklist", back_populates="uav")
    telemetry = relationship("TelemetryData", back_populates="uav")

class PartCategory(BaseModel):
    __tablename__ = "part_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    
    installed_parts = relationship("InstalledPart", back_populates="category")

class InstalledPart(BaseModel):
    """Tracks serialized parts currently installed on a UAV for Lifecycle & Predictive Maintenance"""
    __tablename__ = "installed_parts"
    id = Column(Integer, primary_key=True, index=True)
    uav_id = Column(Integer, ForeignKey("uavs.id"))
    category_id = Column(Integer, ForeignKey("part_categories.id"))
    serial_number = Column(String, unique=True, index=True)
    name = Column(String)
    installation_date = Column(DateTime, default=datetime.utcnow)
    
    max_flight_hours = Column(Float)
    current_flight_hours = Column(Float, default=0.0)
    max_cycles = Column(Integer, nullable=True)
    current_cycles = Column(Integer, default=0)
    
    status = Column(String, default="OK") # OK, Warning, Critical
    
    uav = relationship("UAV", back_populates="parts")
    category = relationship("PartCategory", back_populates="installed_parts")
    work_orders = relationship("WorkOrder", back_populates="part")

class WorkOrder(BaseModel):
    """Squawk Sheet / Damage Report tied to Maker-Checker flow"""
    __tablename__ = "work_orders"
    id = Column(Integer, primary_key=True, index=True)
    uav_id = Column(Integer, ForeignKey("uavs.id"))
    part_id = Column(Integer, ForeignKey("installed_parts.id"), nullable=True)
    
    severity = Column(Integer)  # 1-AOG/Critical, 2-High, 3-Medium, 4-Low
    description = Column(Text)
    action_taken = Column(Text, nullable=True)
    
    technician_id = Column(Integer, ForeignKey("users.id")) # Maker
    engineer_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Checker
    
    # Statuses: Open, Pending Review, Closed
    status = Column(String, default="Open")
    
    uav = relationship("UAV", back_populates="work_orders")
    part = relationship("InstalledPart", back_populates="work_orders")
    technician = relationship("User", foreign_keys=[technician_id], back_populates="work_orders_created")
    engineer = relationship("User", foreign_keys=[engineer_id], back_populates="work_orders_approved")

class PreFlightChecklist(BaseModel):
    """Dynamic check-list filled by technician via QR before flight"""
    __tablename__ = "pre_flight_checklists"
    id = Column(Integer, primary_key=True, index=True)
    uav_id = Column(Integer, ForeignKey("uavs.id"))
    technician_id = Column(Integer, ForeignKey("users.id"))
    
    checklist_data = Column(JSON)  # Stores questions and boolean answers
    is_passed = Column(Boolean, default=False)
    
    uav = relationship("UAV", back_populates="checklists")
    technician = relationship("User", back_populates="checklists")

class TelemetryData(BaseModel):
    """Time-series data from PX4/VOXL logs for Trend Analysis & Predictive Maintenance"""
    __tablename__ = "telemetry_data"
    id = Column(Integer, primary_key=True, index=True)
    uav_id = Column(Integer, ForeignKey("uavs.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    rpm_asymmetry = Column(Float, nullable=True)
    esc_temperature = Column(Float, nullable=True)
    vibration_level = Column(Float, nullable=True)
    battery_level = Column(Float, nullable=True)
    
    uav = relationship("UAV", back_populates="telemetry")
