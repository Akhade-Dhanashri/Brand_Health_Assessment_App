from sqlalchemy import Column, Integer, String, DateTime, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Base class for SQLAlchemy models
Base = declarative_base()

# Submission model
class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    company = Column(String, nullable=False)
    responses_json = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)
    percentage = Column(Integer, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)

# SQLite database setup
database_url = "sqlite:///./submissions.db"
engine = create_engine(database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the table in the database (if not exists)
Base.metadata.create_all(bind=engine)
