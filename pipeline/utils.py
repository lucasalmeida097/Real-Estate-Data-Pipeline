from unidecode import unidecode
from bs4.element import Tag
from typing import Optional
import logging
import os

logger = logging.getLogger(__name__)
BASE_URL = os.getenv("BASE_URL")


def extract_property_info(card: Tag) -> Optional[dict]:
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
