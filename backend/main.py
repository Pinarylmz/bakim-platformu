import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import models, database
from database import engine
from routers import uav, inventory, damage, auth, audit, users, telemetry
from fastapi.staticfiles import StaticFiles
import os

os.makedirs("uploads", exist_ok=True)

from seed import seed_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables and run conditional seeding on startup
    models.Base.metadata.create_all(bind=engine)
    try:
        seed_database()
    except Exception as e:
        print(f"Skipping seed due to error or already seeded: {e}")
    yield

app = FastAPI(title="Enterprise UAV Maintenance Platform", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(uav.router)
app.include_router(inventory.router)
app.include_router(damage.router)
app.include_router(audit.router)
app.include_router(users.router)
app.include_router(telemetry.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
