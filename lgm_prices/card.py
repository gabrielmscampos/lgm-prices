from typing import Tuple

from bs4 import BeautifulSoup

from .utils import parse_currency


class Card:
    DEFAULT_URL = "https://www.ligamagic.com.br/"

    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    def seller(self) -> str:
        """
        Get seller name
        """
        return self.soup\
            .find("div", {"class": "e-col1"})\
            .find("img")["title"]

    def edition_and_extras(self) -> Tuple:
        """
        Get card edition
        """
        col2 = self.soup.find("div", {"class": "e-col2"})
        edicao_extras = col2.find_all("div", {"class": "edicaoextras"})

        if len(edicao_extras) > 0:
            extras = edicao_extras[0].find("p", {"class": "extras"}).text.split(", ")
            edition = edicao_extras[0].find("a", {"class": "ed-simb"}).text
        else:
            extras = []
            edition = col2.find("font", {"class": "nomeedicao"})["title"]

        return edition, extras

    def prices(self) -> Tuple:
        """
        Get card prices
        """
        price_div = self.soup.find("div", {"class": "e-col3"})
        img_monet_div = price_div.find_all("div", {"class": "imgnum-monet"})
        price_sale_div = price_div.find_all("font", {"class": "mob-preco-desconto"})

        image_classes = []
        og_price = None
        on_sale = len(price_sale_div) > 0
        is_price_image = len(img_monet_div) > 0

        if is_price_image:
            price_image_divs = price_div.find_all("div")
            price = [div for div in price_image_divs if div.text == "\xa0"]
            price = [" ".join(div["class"]) if div.has_attr("class") else "," for div in price]
            image_classes = [div for div in price_image_divs if div.has_attr("class")]
            image_classes = [div["class"] for div in image_classes if div.text == "\xa0"]
        elif on_sale:
            prices_text = price_div.text
            og_price_text = price_sale_div[0].text
            price_text = prices_text.replace(og_price_text, "")
            price_text = og_price_text if price_text == "" else price_text
            og_price = parse_currency(og_price_text)
            price = parse_currency(price_text)
        else:
            price = parse_currency(price_div.text)

        return on_sale, is_price_image, og_price, price, image_classes

    def language_and_condition(self) -> Tuple:
        """
        Get card language
        """
        col4 = self.soup.find("div", {"class": "e-col4"})
        lang = col4.find("img")["title"]
        condition = col4.find("font").text
        return lang, condition

    def get_href_to_store(self) -> str:
        """
        Get store name from card web element
        """
        return self.DEFAULT_URL \
                + self.soup.\
                    find("div", {"class": "e-col7"})\
                        .find("a")["href"]
