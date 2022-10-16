from PIL import Image


def find(func, iterator):
    for value in iterator:
        if func(value):
            return value


def parse_currency(text: str) -> float:
    """
    Parse currency string into number (R$ 123,2 -> 123.2)
    """
    value = text.strip().split()[-1]
    return float(value.replace(".", "").replace(",", "."))


def resize(img: Image, new_height: int) -> Image:
    new_width = int(new_height * img.width / img.height)
    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
