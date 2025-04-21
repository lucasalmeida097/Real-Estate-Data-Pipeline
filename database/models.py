from sqlalchemy import Column, Integer, Text, Numeric, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class RealEstate(Base):
    __tablename__ = "real_estate"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    price = Column(Numeric(12, 2))
    size = Column(Integer)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    parking_spaces = Column(Integer)
    link = Column(Text, unique=True)

    def __repr__(self):
        return (
            f"<RealEstate(title='{self.title}', price={self.price},"
            f"link='{self.link}')>"
        )


class ScrapingStatus(Base):
    __tablename__ = "scraping_status"

    id = Column(Integer, primary_key=True, index=True)
    last_update = Column(DateTime, default=datetime.utcnow)
    total_properties = Column(Integer)
    status = Column(String, default="success")
    message = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<ScrapingStatus(id={self.id}, last_update={self.last_update},"
            f"status={self.status})>"
        )
