import json

from lgm_prices.marketplace import Marketplace
from lgm_prices.card import Card
from lgm_prices.image import PriceRecognizer

HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Methods": "OPTIONS,GET",
    "Content-Type": "application/json"
}


def handler(event, context):
    """
    """
    params = event.get("queryStringParameters", {})
    card_name = params.get("card")

    if card_name is None:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Bad request",
                "ex": "Missing card queryStringParameter"
            }),
            "headers": HEADERS
        }

    try:
        mkt = Marketplace(card_name)
        mkt.open()
    except Exception as err:
        return {
            "statusCode": 503,
            "body": json.dumps({
                "error": "Failed to open marketplace.",
                "ex": str(err)
            }),
            "headers": HEADERS
        }

    inventory = mkt.inventory()

    if len(inventory) == 0:
        return {
            "statusCode": 200,
            "body": "[]",
            "headers": HEADERS
        }

    cards = []
    price_css_classes = []
    inline_css = mkt.inline_css()

    for card in inventory:
        card = Card(card)
        seller = card.seller()
        edition, extras = card.edition_and_extras()
        on_sale, is_price_image, og_price, price, image_classes = card.prices()
        lang, condition = card.language_and_condition()
        href = card.get_href_to_store()
        price_css_classes.extend(image_classes)
        cards.append({
            "seller": seller,
            "edition": edition,
            "extras": extras,
            "on_sale": on_sale,
            "og_price": og_price,
            "is_price_image": is_price_image,
            "price": price,
            "language": lang,
            "condition": condition,
            "href": href,
        })

    try:
        recognizer = PriceRecognizer(inline_css, price_css_classes)
    except Exception as err:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Failed to init PriceRecognizer.",
                "ex": str(err)
            }),
            "headers": HEADERS
        }

    assets = recognizer.assets()
    dimensions = recognizer.dimensions()
    coordinates = recognizer.coordinates()
    img_to_number = recognizer.read_numbers_2(assets, dimensions, coordinates)

    # Update cards metadata using image to number dict
    cards = mkt.update_prices(cards, recognizer.asset_id[0], recognizer.dim_id[0], img_to_number)

    return {
        "statusCode": 200,
        "body": json.dumps(cards),
        "headers": HEADERS
    }
