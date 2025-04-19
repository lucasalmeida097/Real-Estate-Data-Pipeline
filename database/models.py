from sqlalchemy import Column, Integer, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base

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
