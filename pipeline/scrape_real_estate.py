from bs4 import BeautifulSoup
import pandas as pd
import logging
import os
import json
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from unidecode import unidecode

logging.basicConfig(level=logging.INFO)
load_dotenv(dotenv_path=".env")
BASE_URL = os.getenv("BASE_URL")
URL = os.getenv("URL")


def extract_property_info(card):
    try:
        title_element = card.select_one("h2.styles-module__aBT18q__heading2")
        title = unidecode(title_element.get_text(strip=True)) if title_element else None

        price_element = card.select_one("p.style-module__Yo5w-q__price b")
        price = price_element.get_text(strip=True) if price_element else None

        details_elements = card.select(
            ".style-module__Yo5w-q__list p.styles-module__aBT18q__body2"
        )
        details = [d.get_text(strip=True) for d in details_elements]

        link_element = card.select_one("a.link-module__x-ue-q__rawLink")
        link = (
            BASE_URL + link_element["href"]
            if link_element and "href" in link_element.attrs
            else None
        )

        return {"title": title, "price": price, "details": details, "link": link}
    except Exception as e:
        logging.error(f"Error extracting property: {e}")
        return None


def collect_properties(total_pages):
    properties = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for current_page in range(1, total_pages + 1):
            url_with_page = f"{URL}?pg={current_page}"
            logging.info(f"Collecting page {url_with_page}")
            page.goto(url_with_page, timeout=60000)

            try:
                page.goto(url_with_page, timeout=60000)
                page.wait_for_selector("#listing", timeout=15000)
                page.wait_for_selector("div[data-template='card']", timeout=15000)
            except TimeoutError as e:
                logging.warning(
                    f"Timeout while loading the page or elements on the page. "
                    f"{current_page}: {e}"
                )
                continue

            soup = BeautifulSoup(page.content(), "html.parser")
            listing_container = soup.select_one("#listing")

            if listing_container:
                cards = listing_container.select("div[data-template='card']")
                logging.info(f"Found {len(cards)} cards on page {current_page}")
                for card in cards:
                    data = extract_property_info(card)
                    if data:
                        properties.append(data)
            else:
                logging.warning("Could not find the listing container.")

        browser.close()

    return properties


def normalize_text_columns(df):
    text_columns = df.select_dtypes(include="object").columns
    for columns in text_columns:
        df[columns] = df[columns].apply(
            lambda x: unidecode(x) if isinstance(x, str) else x
        )
    return df


def clean_properties(properties):
    df = pd.DataFrame(properties)
    df = normalize_text_columns(df)

    subset_columns = ["title", "link"]
    df = df.drop_duplicates(subset=subset_columns)

    df["details"] = df["details"].apply(
        lambda x: json.loads(x) if isinstance(x, str) else x
    )
    df["size"] = df["details"].apply(
        lambda x: int(float(x[0].replace("m²", "").replace(" ", "")))
        if isinstance(x, list) and len(x) > 0
        else None
    )
    df["bedrooms"] = df["details"].apply(
        lambda x: int(x[1].split(" ")[2])
        if isinstance(x, list) and len(x) > 1 and " a " in x[1]
        else (
            int(x[1]) if isinstance(x, list) and len(x) > 1 and x[1].isdigit() else None
        )
    )
    df["parking_spaces"] = df["details"].apply(
        lambda x: int(x[2]) if isinstance(x, list) and len(x) > 2 else None
    )
    df["bathrooms"] = df["details"].apply(
        lambda x: int(x[3]) if isinstance(x, list) and len(x) > 3 else None
    )

    df["price"] = df["price"].astype(str)
    df["price"] = (
        df["price"]
        .str.replace("R$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    df.drop(columns=["details"], inplace=True)

    return df


def save_to_csv(df, csv_path):
    df.to_csv(csv_path, index=False)
    logging.info(f"Saved to {csv_path}")


if __name__ == "__main__":
    num_pages_scraping = 5
    properties = collect_properties(num_pages_scraping)
    if properties:
        df = clean_properties(properties)
        save_to_csv(df, "data/csv/real_estate_sao_paulo.csv")
    else:
        logging.warning("No properties were collected.")
