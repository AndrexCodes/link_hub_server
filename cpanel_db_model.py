from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, time
import random
import string

DB_USERNAME = 'andrew'
DB_PASSWORD = '1234567890'
DB_DATABASE = 'link_hub'

engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_DATABASE}", echo=True)
Base = declarative_base()

def generate_random_code():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(20))


class Link_Hubs(Base):
    __tablename__ = 'users'
    id = Column(String(20), primary_key=True, default=generate_random_code)
    name = Column(String(50), nullable=False)
    state = Column(Boolean,default=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    created_at = Column(DateTime, default=datetime.now)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()