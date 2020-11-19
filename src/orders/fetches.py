from functools import lru_cache

import requests
from django.conf import settings

@lru_cache()
def get_dollar_blue():
    url = settings.DOLAR_BLUE_PRICE
    quotes = requests.get(url).json()
    for _quote in quotes:
        if _quote.get('casa').get('nombre') == 'Dolar Blue':
            quote = float(_quote.get('casa').get('venta').replace(',', '.'))
            break
    return quote