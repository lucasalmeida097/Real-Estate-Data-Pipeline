import os
import logging
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)
load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_db(df, table_name="real_estate"):
    from database.models import RealEstate

    logger.info(f"Saving {len(df)} records to '{table_name}'...")
    db = next(get_db())

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    int_columns = ["size", "bedrooms", "bathrooms", "parking_spaces"]
    for col in int_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    df = df.fillna(pd.NA)

    try:
        records_to_insert = df.to_dict(orient="records")
        for record in records_to_insert:
            existing = db.query(RealEstate).filter_by(link=record.get("link")).first()
            if not existing:
                db_record = RealEstate(**record)
                db.add(db_record)
        db.commit()
        logger.info(f"Successfully inserted {len(records_to_insert)} new records.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error during database insertion: {e}")
