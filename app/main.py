from fastapi import FastAPI, HTTPException, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from enum import Enum

from app import models, crud
from database.db import get_db

app = FastAPI()


class OrderFields(str, Enum):
    price = "price"
    size_sqm = "size_sqm"
    bedrooms = "bedrooms"
    bathrooms = "bathrooms"
    parking_spaces = "parking_spaces"


@app.get("/properties", response_model=List[models.Property])
def get_properties(
    min_price: float = 0,
    max_price: float = 1_000_000,
    size_sqm: int = 0,
    bedrooms: int = 0,
    bathrooms: int = 0,
    parking_spaces: int = 0,
    order_by: Optional[OrderFields] = None,
    order_direction: str = Query("asc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    properties = crud.get_properties(
        db,
        min_price,
        max_price,
        size_sqm,
        bedrooms,
        bathrooms,
        parking_spaces,
        order_by,
        order_direction,
    )
    if not properties:
        raise HTTPException(status_code=404, detail="No properties found.")
    return properties


@app.get("/properties/{property_id}", response_model=models.Property)
def get_property(property_id: int, db: Session = Depends(get_db)):
    property = crud.get_property_by_id(db, property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found.")
    return property


@app.get("/status")
def get_status(db: Session = Depends(get_db)):
    status = crud.get_latest_scraping_status(db)
    if not status:
        raise HTTPException(status_code=404, detail="No status found.")
    return status
