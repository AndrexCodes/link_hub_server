from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, time
import random
import string

DB_USERNAME = 'exchecke_app'
DB_PASSWORD = '{Um?8wQ15W}U'
DB_DATABASE = 'test'

engine = create_engine(f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_DATABASE}", echo=True)
Base = declarative_base()

def generate_random_code():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(5))


class User(Base):
    __tablename__ = 'users'
    id = Column(String(5), primary_key=True, default=generate_random_code)
    name = Column(String(50), nullable=False)
    email = Column(Integer, nullable=False)
    phone = Column(String(13), nullable=False)
    password =  Column(String(200), nullable=False)
    state = Column(Boolean,default=True)
    admin = Column(Boolean,default=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    created_at = Column(DateTime, default=datetime.now)


class Client_Device(Base):
    __tablename__ = 'devices'
    id = Column(String(5), primary_key=True, default=generate_random_code)
    name = Column(String(50), nullable=False)
    state = Column(Boolean,default=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    created_at = Column(DateTime, default=datetime.now)
    schedules = relationship("Schedule", back_populates="device", cascade='all, delete-orphan')


class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(String(5), primary_key=True, default=generate_random_code)
    device_id = Column(String(5), ForeignKey('devices.id'), nullable=False)
    name = Column(String(50), nullable=False)
    execute_at = Column(Time)
    duration = Column(Integer, default=30) # Time in seconds
    state = Column(Boolean,default=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    created_at = Column(DateTime, default=datetime.now)
    device = relationship("Client_Device", back_populates="schedules")


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# device_1 = Client_Device(name="Dinning Hall Bell", state=True)
# device_2 = Client_Device(name="Tution Block Bell", state=True)
# device_3 = Client_Device(name="Dormitory Area Bell", state=True)

# session.add_all([device_1, device_2, device_3])

# device = session.query(Client_Device).filter_by(id="5Ib7g").first()
# schedule = Schedule(name="Wake Up Time", execute_at=time(12, 30), duration=10, state=True, device=device)
# session.add(schedule)
# session.commit()

# device = session.query(Client_Device).filter_by(id="5Ib7g").first()
# print(device.schedules)
# for x in device.schedules:
#     print(x.name)

# from passlib.hash import sha256_crypt

# user = User(
#     name="Andrew Macharia", 
#     email="machariaandrew1428@gmail.com",
#     phone="254795359098",
#     password=sha256_crypt.hash("1234")
#     )

# session.add(user)
# session.commit()
