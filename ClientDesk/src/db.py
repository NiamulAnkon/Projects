from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.models import Base

DATABASE_URL = "sqlite:///Database/invoices.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Add missing columns to existing tables
    with engine.connect() as connection:
        # Check if status column exists in clients table
        try:
            connection.execute(text("ALTER TABLE clients ADD COLUMN status VARCHAR(20) DEFAULT 'pending'"))
            connection.commit()
        except Exception:
            # Column already exists
            pass

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()