import requests
import json
from config import keys

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f"Невозможно осуществить конвертацию валюты одного и то же наименования {base}.")
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}")
        try:
            amount = str(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}")

        r = requests.get(f'https://v6.exchangerate-api.com/v6/af4c65dd57ce550e76041503/pair/{quote_ticker}/{base_ticker}')
        total_base = json.loads(r.content)["conversion_rate"] * float(amount)
        return total_base