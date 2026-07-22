from database import engine, SessionLocal
import models
from datetime import datetime, timedelta

def seed_database():
    print("Creating tables...")
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # 1. Check if seeded
    if db.query(models.User).count() > 0:
        print("Database already seeded.")
        db.close()
        return

    print("Seeding Users/Roles...")
    # Seed Users
    admin = models.User(full_name="System Admin", username="admin", password_hash="adminpass", role="Admin", approval_status="Approved", total_time_spent=0)
    engineer = models.User(full_name="John Engineer", username="engineer1", password_hash="engpass", role="Engineer", approval_status="Approved", total_time_spent=0)
    tech = models.User(full_name="Mike Tech", username="tech1", password_hash="techpass", role="Technician", approval_status="Approved", total_time_spent=0)
    
    db.add_all([admin, engineer, tech])
    db.commit()
    
    print("Seeding Part Categories...")
    
    categories = [
        "Ana Rotor Sistemi",
        "Kuyruk Rotoru Sistemi",
        "Güç Aktarma",
        "Motor / Güç Ünitesi",
        "Uçuş Kontrol",
        "Elektronik/Aviyonik",
        "Gövde ve İniş",
        "Enerji ve Haberleşme"
    ]
    
    cat_objs = {}
    for cat in categories:
        c = models.PartCategory(name=cat, description=f"{cat} parçaları")
        db.add(c)
        cat_objs[cat] = c
    
    db.commit()
    for c in cat_objs.values():
        db.refresh(c)
        
    print("Seeding UAVs...")
    # Seed UAV
    uav1 = models.UAV(serial_number="QR-HELI-001", model_name="Alpha-X", total_flight_hours=450.5, total_flight_cycles=120)
    db.add(uav1)
    db.commit()
    db.refresh(uav1)
    
    print("Seeding Installed Parts...")
    
    # Adding a realistic helicopter part for each category
    parts_to_add = [
        (cat_objs["Ana Rotor Sistemi"].id, "ROT-1122", "Ana rotor kanatları (Titanium)", 1000.0, 450.5, "OK"),
        (cat_objs["Kuyruk Rotoru Sistemi"].id, "TR-4455", "Kuyruk rotoru göbeği", 800.0, 200.0, "OK"),
        (cat_objs["Güç Aktarma"].id, "GB-9900", "Ana dişli kutusu", 1500.0, 450.5, "OK"),
        (cat_objs["Motor / Güç Ünitesi"].id, "MOT-8899", "Fırçasız motor (BLDC v3)", 500.0, 480.0, "Warning"),
        (cat_objs["Uçuş Kontrol"].id, "FC-1010", "Uçuş kontrol kartı (FC)", 2000.0, 450.5, "OK"),
        (cat_objs["Elektronik/Aviyonik"].id, "AV-3322", "Kamera/Gimbal Modülü", 600.0, 100.0, "OK"),
        (cat_objs["Gövde ve İniş"].id, "LD-777", "İniş takımı (Amortisörlü)", 1200.0, 450.5, "OK"),
        (cat_objs["Enerji ve Haberleşme"].id, "BAT-001", "LiPo/Li-Ion batarya", 300.0, 280.0, "Warning"),
    ]
    
    installed_parts = []
    for p in parts_to_add:
        cat_id, sn, name, m_hrs, c_hrs, status = p
        installed_parts.append(models.InstalledPart(
            uav_id=uav1.id, category_id=cat_id, serial_number=sn, name=name,
            max_flight_hours=m_hrs, current_flight_hours=c_hrs,
            max_cycles=int(m_hrs/2), current_cycles=int(c_hrs/2), status=status
        ))
        
    db.add_all(installed_parts)
    db.commit()
    
    # Find the motor to attach the work order to
    motor_part = next(p for p in installed_parts if p.serial_number == "MOT-8899")
    
    print("Seeding AOG Work Order...")
    wo = models.WorkOrder(
        uav_id=uav1.id,
        part_id=motor_part.id,
        severity=1, # 1-Critical/AOG
        description="Motor temperature abnormal, vibration detected in PX4 logs. Requires immediate replacement.",
        technician_id=tech.id,
        status="Pending Review"
    )
    db.add(wo)
    
    # Audit log
    log = models.SystemLog(
        user_id=tech.id, action="CREATE_WORK_ORDER", target_table="work_orders", 
        details="AOG squawk created for MOT-8899"
    )
    db.add(log)
    
    db.commit()
    db.close()
    print("Database initialization and seeding complete.")

if __name__ == "__main__":
    seed_database()
