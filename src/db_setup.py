from sqlalchemy import create_engine, Column, Integer, String, Date, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class MaintenanceLog(Base):
    __tablename__ = 'maintenance_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    aircraft_id = Column(String(50), nullable=False)
    event_date = Column(Date, nullable=True) # Date is standard YYYY-MM-DD
    error_code = Column(String(20), nullable=True) # Extracted Regex
    description = Column(Text, nullable=True)
    technician = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    parts_replaced = Column(String(100), nullable=True)
    source_file = Column(String(100), nullable=True) # Audit trail
    processed_at = Column(Date, default=datetime.datetime.utcnow)

def init_db():
    DATABASE_URL = "sqlite:///maintenance.db"
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print(f"Database initialized at {DATABASE_URL}")

if __name__ == "__main__":
    init_db()
