from sqlalchemy import Column, Integer, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RealEstate(Base):
    __tablename__ = "real_estate"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    price = Column(Numeric(12, 2), nullable=True)
    size = Column(Integer, nullable=True)
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    parking_spaces = Column(Integer, nullable=True)
    link = Column(Text, unique=True, nullable=True)

    def __repr__(self):
        return (
            f"<RealEstate(id={self.id}, title={self.title}, price={self.price}, "
            f"size={self.size}, bedrooms={self.bedrooms}, bathrooms={self.bathrooms}, "
            f"parking_spaces={self.parking_spaces}, link={self.link})>"
        )
