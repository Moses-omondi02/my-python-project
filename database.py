from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from alembic import command
from alembic.config import Config

def init_db():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


DATABASE_URL = 'sqlite:///voter_registration.db'

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    from models import Voter, VoterLoginCredentials, VoterAddress  
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def drop_db():
    """Drop all database tables"""
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped successfully!")