from sqlalchemy import Column, String, Integer, Float, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Vehicle(Base):
    __tablename__ = "vehicles"

    vin = Column(String(17), primary_key=True, index=True)
    manufacturer_name = Column(String(255), nullable=False)
    description = Column(String)
    horse_power = Column(Integer)
    model_name = Column(String(255))
    model_year = Column(Integer)
    purchase_price = Column(Float)
    fuel_type = Column(String(50))
