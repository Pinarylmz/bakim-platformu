import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Check for Railway Database URLs
DATABASE_URL = os.getenv("DATABASE_URL")
MYSQL_URL = os.getenv("MYSQL_URL")

connect_args = {}

if DATABASE_URL:
    # Fix for SQLAlchemy 1.4+ which requires postgresql:// instead of postgres://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URL = DATABASE_URL
elif MYSQL_URL:
    # Ensure MySQL uses PyMySQL driver
    if MYSQL_URL.startswith("mysql://"):
        MYSQL_URL = MYSQL_URL.replace("mysql://", "mysql+pymysql://", 1)
    SQLALCHEMY_DATABASE_URL = MYSQL_URL
else:
    # Fallback to local SQLite
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'maintenance.db')}"
    connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
