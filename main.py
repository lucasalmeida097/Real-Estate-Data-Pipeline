import logging
from dotenv import load_dotenv
from pipeline.scraper import collect_properties
from pipeline.cleaner import clean_properties
from pipeline.csv_writer import save_to_csv

load_dotenv()
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    NUM_PAGES = 5
    CSV_PATH = "data/csv/real_estate_sao_paulo.csv"

    properties = collect_properties(NUM_PAGES)

    if properties:
        df = clean_properties(properties)
        save_to_csv(df, CSV_PATH)
    else:
        logging.warning("No properties were collected.")
