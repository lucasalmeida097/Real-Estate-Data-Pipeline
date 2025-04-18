import pandas as pd
import logging

logger = logging.getLogger(__name__)


def save_to_csv(df: pd.DataFrame, csv_path: str):
    df.to_csv(csv_path, index=False)
    logging.info(f"Saved cleaned data to {csv_path}")
