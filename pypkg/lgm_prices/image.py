from io import BytesIO
from typing import Dict, List
import pkg_resources

import requests
from more_itertools import flatten
from PIL import Image, ImageDraw, ImageFont
from pytesseract import image_to_string

from .utils import resize, find


class PriceRecognizer:
    DEFAULT_FONT = ImageFont.truetype(
        pkg_resources.resource_filename(__name__, "data/esparac.ttf"), 13
    )

    def __init__(self, inline_css: Dict, price_css_classes: List):
        price_css_classes = list(set(flatten(price_css_classes)))
        self.price_css_classes = {
            key: value
            for key, value in inline_css.items()
            if key in price_css_classes
        }
        self.asset_id = self.__get_id("background-image")
        self.dim_id = self.__get_id("width")

    @staticmethod
    def __crop(img, coords, dim):
        """
        """
        return img.crop(
            (
                -1*coords.get("x"),
                -1*coords.get("y"),
                -1*coords.get("x") + dim.get("width"),
                -1*coords.get("y") + dim.get("height")
            )
        )

    def __process_image(self, img):
        """
        """
        img = resize(img, int(img.height*1.5))
        new_img = Image.new("RGBA", (img.width*10, img.height*3), "WHITE")
        x1 = int(new_img.width*0.8) - int(img.width*0.8)
        x2 = int(new_img.width*0.1)
        y1 = int(new_img.height*0.5) - int(img.height*0.5)
        y2 = int(new_img.height*0.5) - 5
        new_img.paste(img, (x1,y1))

        # Write "number: " before number image to help tesseract
        d1 = ImageDraw.Draw(new_img)
        d1.text((x2, y2), "number: ", (0, 0, 0), self.DEFAULT_FONT)

        return new_img

    def __get_id(self, tag: str):
        """
        """
        res = find(lambda x: x[1].startswith(tag), self.price_css_classes.items())
        self.price_css_classes.pop(res[0])
        return res

    def assets(self):
        """
        """
        url = self.asset_id[1].replace("background-image: url(//", "https://").replace(")", "")
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGBA")
        assets = Image.new("RGBA", img.size, "WHITE")
        assets.paste(img, (0, 0), img)
        return assets

    def dimensions(self):
        """
        """
        tmp = self.dim_id[1].split("\n")
        dim = {
            "width": int(tmp[0].split(" ")[-1].replace("px;", "")),
            "height": int(tmp[2].split(" ")[-1].replace("px", ""))
        }
        return dim

    def coordinates(self):
        """
        """
        return {
            key: {
                "x": int(value.split(" ")[1].replace("px", "")),
                "y": int(value.split(" ")[2].replace("px", ""))
            }
            for key, value in self.price_css_classes.items()
        }

    def read_numbers(self, assets, dimensions, coordinates):
        """
        """
        result = {}
        images = {
            id_number: self.__crop(assets, coords, dimensions)
            for id_number, coords in coordinates.items()
        }

        for id_number, img in images.items():
            processed_img = self.__process_image(img)
            processed_number = image_to_string(processed_img)
            result[id_number] = processed_number.strip().split(" ")[-1]

        return result

    def read_numbers_2(self, assets, dimensions, coordinates):
        """
        """
        images = {
            id_number: self.__crop(assets, coords, dimensions)
            for id_number, coords in coordinates.items()
        }
        images_obj = list(images.values())

        # Concat all images into one image
        new_width = sum([img.width for img in images_obj])
        new_height = max([img.height for img in images_obj])
        new_img = Image.new('RGB', (new_width, new_height))

        acc_width = 0
        for img in images_obj:
            new_img.paste(img, (acc_width, 0))
            acc_width += img.width

        new_img = resize(new_img, int(new_img.height*1.5))
        numbers = image_to_string(new_img).strip()
        return dict(zip(images.keys(), list(numbers)))
