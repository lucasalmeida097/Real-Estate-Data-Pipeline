from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PropertyBase(BaseModel):
    title: str
    price: float
    size_sqm: Optional[str]
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    parking_spaces: Optional[int]
    link: str


class Property(PropertyBase):
    id: int

    class Config:
        orm_mode: True


class ScrapingStatusResponse(BaseModel):
    last_update: datetime
    total_properties: int
    status: str
    message: Optional[str] = None

    class Config:
        orm_mode = True
