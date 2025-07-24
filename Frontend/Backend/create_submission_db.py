from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    company = Column(String(100))
    responses = Column(Text)
    score = Column(Integer)

# Create SQLite database
engine = create_engine("sqlite:///submissions.db", echo=True)
Base.metadata.create_all(bind=engine)

print("✅ submissions.db and table created successfully.")
