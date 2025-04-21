from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from database.models import RealEstate, ScrapingStatus
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


def get_properties(
    db: Session,
    min_price: float,
    max_price: float,
    size_sqm: int,
    bedrooms: int,
    bathrooms: int,
    parking_spaces: int,
    order_by: str = None,
    order_direction: str = "asc",
):
    query = db.query(RealEstate).filter(
        RealEstate.price >= min_price,
        RealEstate.price <= max_price,
        RealEstate.size >= size_sqm,
        RealEstate.bedrooms >= bedrooms,
        RealEstate.bathrooms >= bathrooms,
        RealEstate.parking_spaces >= parking_spaces,
    )

    if order_by:
        column = getattr(RealEstate, order_by, None)
        if column is not None:
            direction = asc if order_direction == "asc" else desc
            query = query.order_by(direction(column))

    return query.all()


def get_property_by_id(db: Session, property_id: int):
    return db.query(RealEstate).filter(RealEstate.id == property_id).first()


def get_latest_scraping_status(db: Session):
    return db.query(ScrapingStatus).order_by(ScrapingStatus.last_update.desc()).first()


def create_scraping_status(
    db: Session, total_properties: int, status: str, message: str = None
):
    scraping_status = ScrapingStatus(
        last_update=datetime.now(tz=timezone.utc),
        total_properties=total_properties,
        status=status,
        message=message,
    )
    db.add(scraping_status)
    db.commit()
    db.refresh(scraping_status)
    return scraping_status


def log_scraping_status(
    db: Session, total_properties: int, status: str, message: str = None
):
    try:
        create_scraping_status(
            db=db, total_properties=total_properties, status=status, message=message
        )
    except Exception as e:
        logger.error(f"Failed to save status '{status}' to the database: {e}")
