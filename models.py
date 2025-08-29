from sqlalchemy import Column, String, Date, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, validates
from database import Base
from datetime import datetime, date
import uuid

class Voter(Base):
    __tablename__ = 'voters'
    
    voter_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    national_id_number = Column(String(20), nullable=False, unique=True)
    title = Column(String(10))
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    registration_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    credentials = relationship("VoterLoginCredentials", back_populates="voter", uselist=False, cascade="all, delete-orphan")
    addresses = relationship("VoterAddress", back_populates="voter", cascade="all, delete-orphan")
    
    @validates('national_id_number')
    def validate_national_id(self, key, national_id):
        if not national_id or len(national_id) < 5:
            raise ValueError("National ID must be at least 5 characters long")
        return national_id
    
    @validates('first_name', 'last_name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError(f"{key} cannot be empty")
        return name.strip()
    
    @validates('date_of_birth')
    def validate_dob(self, key, dob):
        if isinstance(dob, str):
            dob = datetime.strptime(dob, '%Y-%m-%d').date()
        if dob > date.today():
            raise ValueError("Date of birth cannot be in the future")
        if (date.today().year - dob.year) < 18:
            raise ValueError("Voter must be at least 18 years old")
        return dob

class VoterLoginCredentials(Base):
    __tablename__ = 'voter_login_credentials'
    
    voter_id = Column(String(36), ForeignKey('voters.voter_id', ondelete='CASCADE'), primary_key=True)
    password = Column(String(255), nullable=False)
    last_password_change = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    voter = relationship("Voter", back_populates="credentials")
    
    @validates('password')
    def validate_password(self, key, password):
        if len(password) < 4:
            raise ValueError("Password must be at least 4 characters long")
        return password

class VoterAddress(Base):
    __tablename__ = 'voter_address'
    
    address_id = Column(BigInteger, primary_key=True, autoincrement=True)
    voter_id = Column(String(36), ForeignKey('voters.voter_id', ondelete='CASCADE'), nullable=False)
    address_line_1 = Column(String(255), nullable=False)
    ward = Column(String(100), nullable=False)
    subcounty = Column(String(100), nullable=False)
    county = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(2), nullable=False)
    address_type = Column(String(20), nullable=False)
    
    voter = relationship("Voter", back_populates="addresses")
    
    @validates('country')
    def validate_country(self, key, country):
        if len(country) != 2 or not country.isalpha():
            raise ValueError("Country must be a 2-letter code")
        return country.upper()
    
    @validates('postal_code')
    def validate_postal_code(self, key, postal_code):
        if not postal_code or len(postal_code.strip()) == 0:
            raise ValueError("Postal code cannot be empty")
        return postal_code.strip()