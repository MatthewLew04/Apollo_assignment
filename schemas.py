from pydantic import BaseModel
from typing import Optional


class VehicleBase(BaseModel):
    manufacturer_name: str
    description: Optional[str] = None
    horse_power: Optional[int] = None
    model_name: Optional[str] = None
    model_year: Optional[int] = None
    purchase_price: Optional[float] = None
    fuel_type: Optional[str] = None


class VehicleCreate(VehicleBase):
    pass


class Vehicle(VehicleBase):
    vin: str  # Including the VIN as part of the response model

    class Config:
        orm_mode = True  # Tells Pydantic to treat SQLAlchemy models as dictionaries
