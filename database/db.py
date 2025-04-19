import os
import logging
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


def connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        return conn
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        raise


def save_db(df: pd.DataFrame, table_name: str = "real_estate"):
    conn = connection()
    cursor = conn.cursor()

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        title TEXT,
        price NUMERIC,
        size INTEGER,
        bedrooms INTEGER,
        bathrooms INTEGER,
        parking_spaces INTEGER,
        link TEXT UNIQUE
    );
    """
    cursor.execute(create_table_query)

    insert_query = f"""
    INSERT INTO {table_name} (title, price, size, bedrooms, bathrooms,
    parking_spaces, link)
    VALUES %s
    """

    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    int_columns = ["size", "bedrooms", "bathrooms", "parking_spaces"]
    for col in int_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    df = df.astype(object)
    data = (
        df[
            [
                "title",
                "price",
                "size",
                "bedrooms",
                "bathrooms",
                "parking_spaces",
                "link",
            ]
        ]
        .where(pd.notnull(df), None)
        .values.tolist()
    )

    try:
        execute_values(cursor, insert_query, data)
        conn.commit()
        logger.info(f"Successfully inserted {len(df)} records into '{table_name}'")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error inserting data: {e}")
    finally:
        cursor.close()
        conn.close()
