from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Vehicle as VehicleModel, Base
from database import engine, SessionLocal
from typing import List
from schemas import Vehicle, VehicleCreate

import random
import string

app = FastAPI()

# Dependency to get the DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables in the database (optional if already created)
Base.metadata.create_all(bind=engine)

# CRUD operations


def get_vehicle(db: Session, vin: str):
    return db.query(VehicleModel).filter(VehicleModel.vin == vin).first()


def get_vehicles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(VehicleModel).offset(skip).limit(limit).all()


def create_vehicle(db: Session, vehicle: VehicleCreate):
    vin = vehicle.vin if vehicle.vin else generate_vin()

    # Check for duplicate VIN if manually provided
    if vehicle.vin:
        existing_vehicle = db.query(VehicleModel).filter(
            VehicleModel.vin == vin).first()
        if existing_vehicle:
            raise HTTPException(status_code=422, detail="VIN already exists")

    db_vehicle = VehicleModel(
        vin=vin,  # Generate or get VIN here (e.g., UUID)
        manufacturer_name=vehicle.manufacturer_name,
        description=vehicle.description,
        horse_power=vehicle.horse_power,
        model_name=vehicle.model_name,
        model_year=vehicle.model_year,
        purchase_price=vehicle.purchase_price,
        fuel_type=vehicle.fuel_type,
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


def update_vehicle(db: Session, vin: str, vehicle: VehicleCreate):
    db_vehicle = db.query(VehicleModel).filter(VehicleModel.vin == vin).first()
    if db_vehicle:
        db_vehicle.manufacturer_name = vehicle.manufacturer_name
        db_vehicle.description = vehicle.description
        db_vehicle.horse_power = vehicle.horse_power
        db_vehicle.model_name = vehicle.model_name
        db_vehicle.model_year = vehicle.model_year
        db_vehicle.purchase_price = vehicle.purchase_price
        db_vehicle.fuel_type = vehicle.fuel_type
        db.commit()
        db.refresh(db_vehicle)
        return db_vehicle
    return None


def delete_vehicle(db: Session, vin: str):
    db_vehicle = db.query(VehicleModel).filter(VehicleModel.vin == vin).first()
    if db_vehicle:
        db.delete(db_vehicle)
        db.commit()
        return True
    return False

# Routes


@app.get("/vehicle", response_model=List[Vehicle])
def read_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vehicles = get_vehicles(db, skip=skip, limit=limit)
    return vehicles


@app.post("/vehicle", response_model=Vehicle, status_code=201)
def create_vehicle_endpoint(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    db_vehicle = create_vehicle(db, vehicle)
    return db_vehicle


@app.get("/vehicle/{vin}", response_model=Vehicle)
def read_vehicle(vin: str, db: Session = Depends(get_db)):
    db_vehicle = get_vehicle(db, vin)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle


@app.put("/vehicle/{vin}", response_model=Vehicle)
def update_vehicle_endpoint(vin: str, vehicle: VehicleCreate, db: Session = Depends(get_db)):
    db_vehicle = update_vehicle(db, vin, vehicle)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle


@app.delete("/vehicle/{vin}", status_code=204)
def delete_vehicle_endpoint(vin: str, db: Session = Depends(get_db)):
    if not delete_vehicle(db, vin):
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {"detail": "Vehicle deleted"}


def generate_vin():
    """Generates a unique, valid 17-character alphanumeric VIN ."""
    allowed_letters = "ABCDEFGHJKLMNPQRSTUVWXYZ"  # Excludes I, O, Q
    allowed_digits = string.digits  # Digits 0-9
    valid_characters = allowed_digits + allowed_letters
    # Select 17 random characters

    vin = ''.join(random.choices(valid_characters, k=17))
    return vin
