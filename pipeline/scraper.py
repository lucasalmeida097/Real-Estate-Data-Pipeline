from bs4 import BeautifulSoup
import logging
from playwright.sync_api import sync_playwright
from .utils import extract_property_info
import os
from database.db import get_db
from app.crud import log_scraping_status


logger = logging.getLogger(__name__)
URL = os.getenv("URL")
# BASE_URL = os.getenv("BASE_URL")


def collect_properties(total_pages: int) -> list[dict]:
    properties = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            for current_page in range(1, total_pages + 1):
                url_with_page = f"{URL}?pg={current_page}"
                logging.info(f"Collecting page {url_with_page}")
                try:
                    page.goto(url_with_page, timeout=60000)
                    page.wait_for_selector("#listing", timeout=15000)
                    page.wait_for_selector("div[data-template='card']", timeout=15000)
                except Exception as e:
                    logging.error(f"Failed to access: {url_with_page}. Error: {e}")
                    page.screenshot(
                        path=f"logs/screenshots/error_page_{current_page}.png",
                        full_page=True,
                    )

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
        finally:
            browser.close()

    db = next(get_db())
    total_collected = len(properties)
    try:
        if total_collected == 0:
            log_scraping_status(
                db=db,
                total_properties=0,
                status="empty",
                message="Scraping completed but returned no properties.",
            )
            logger.warning("No properties collected. Registering status as 'empty'.")
        else:
            log_scraping_status(
                db=db, total_properties=total_collected, status="success"
            )
    except Exception as e:
        log_scraping_status(db=db, total_properties=0, status="error", message=str(e))
        logging.error(f"Failed to save scraping status to the database: {e}")
    return properties
