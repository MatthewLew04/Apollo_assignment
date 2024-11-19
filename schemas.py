from pydantic import BaseModel, Field
from typing import Optional
from pydantic.config import ConfigDict  # Import for model_config


class VehicleBase(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    manufacturer_name: Optional[str] = None
    description: Optional[str] = None
    horse_power: Optional[int] = None
    model_name: Optional[str] = None
    model_year: Optional[int] = None
    purchase_price: Optional[float] = None
    fuel_type: Optional[str] = None
    color: Optional[str] = None
    category: Optional[str] = None


# class VehicleCreate(VehicleBase):
#     pass

# We want VehicleCreate to be required and have vin be an optional part
# This is because we want to have a relatively filled in database, and if they
# input an optional vin, it must match the pattern - which is all upppercase(^),
# and no O, Q, and I to prevent confusion:
# https://en.wikipedia.org/wiki/Vehicle_identification_number
class VehicleCreate(BaseModel):
    model_config = ConfigDict(protected_namespaces=(
    ), from_attributes=True)

    vin: Optional[str] = Field(
        None, max_length=17, pattern="^[A-HJ-NPR-Z0-9]{17}$")  # Optional VIN
    manufacturer_name: str = Field(..., max_length=255)  # Required
    description: str = Field(...)
    horse_power: int = Field(..., gt=0)  # Positive integer - no negative
    # horsepower
    model_name: str = Field(..., max_length=255)  # Required field
    model_year: int = Field(..., ge=1886)  # The first car was made in 1886 -
    # can't have any cars made before then
    purchase_price: float = Field(..., gt=0.0)  # Positive float
    fuel_type: str = Field(..., max_length=50)
    color: str = Field(...)
    category: str = Field(...)


class Vehicle(VehicleBase):
    vin: str  # Including the VIN as part of the response model

    model_config = ConfigDict(from_attributes=True)
