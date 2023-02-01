import json
import requests
from Config import keys


class APIException(Exception):
    pass


class Exchanger:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Неверное название валюты {base}')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Неверное название валюты {quote}')

        if quote == base:
            raise APIException(f'Введите различные названия валют: {base}.')
        try:
            amount = float(amount)

        except ValueError:
            if type(amount) == str:
                raise APIException(f'Введите количество числом, а не текстом')
            if type(amount) == float:
                raise APIException(f'Количество должно быть целым числом либо записано через точку')
            else:
                raise APIException(f'Количество валюты введено неверно {amount}')
            #

        if amount < 0:
            raise APIException(f'Вы ввели отрицательное количество валюты. Попробуйте еще раз')

        if amount == float('inf'):
            raise APIException(f'Вы ввели недопустимо длинное число')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        total_base = total_base * amount

        return total_base
