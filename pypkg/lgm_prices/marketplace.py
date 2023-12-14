import urllib.parse
from typing import List, Dict

import requests
from bs4 import BeautifulSoup
from cssutils import parseString as cssParser

from .utils import parse_currency


class FailedToOpenMarketplace(Exception):
    ...


class CardPageNotFound(Exception):
    ...


class Marketplace:
    DEFAULT_URL = "https://www.ligamagic.com.br/?view=cards/card&card="
    DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"

    def __init__(self, card_name: str) -> None:
        self.card_name = card_name
        self.url = self.DEFAULT_URL + urllib.parse.quote(card_name)
        self.page = None

    def open(self):
        """
        Get card's martketplace html
        """
        session = requests.Session()
        session.headers["User-Agent"] = self.DEFAULT_USER_AGENT
        html = session.get(self.url).content
        self.page = BeautifulSoup(html, "html.parser")

    def inline_css(self) -> Dict[str, str]:
        """
        Extract inline CSS with price numbers image coordinates and asset url
        """
        css = {}
        inline_css = self.page.find_all("link")[6].find("style")

        if inline_css:
            sheet = cssParser(inline_css.text)
            for rule in sheet:
                selector = rule.selectorText
                styles = rule.style.cssText
                css[selector.replace(".", "")] = styles

        return css

    def inventory(self) -> List:
        """
        Get inventory of cards
        """
        return self.page.find_all("div", {"class": "ecom-marketplace", "mp": "1"})

    def update_prices(self, inventory, assets, dimensions, numbers: Dict):
        """
        """
        for card in inventory:
            if card.get("is_price_image"):
                price = card.get("price")
                price = [classes.replace(assets, "").replace(dimensions, "").strip() for classes in price]
                price = parse_currency("".join([numbers.get(_class, _class) for _class in price]))
                card["price"] = price

        return inventory
