# -*- coding: utf-8 -*-

import requests
from config import currency
from tokens import api_key
from config import api_url


######################################################################################################################


class APIException(Exception):
    pass


######################################################################################################################


class ClassBot:
    @staticmethod
    def data_process(message):
        values = message.text.split()
        if len(values) < 2:
            raise APIException(f'Для показа курса, необходимо указать две различные валюты из списка (/values).')
        elif len(values) == 2:
            return ClassBot.get_price(base=values[0].upper(), quote=values[1].upper(), amount=1)
        else:
            return ClassBot.get_price(base=values[0].upper(), quote=values[1].upper(), amount=values[2])

    @staticmethod
    def get_list_currency():
        return '\n'.join(f'{key} - {value}' for key, value in sorted(currency.items()))

    @staticmethod
    def get_price(base, quote, amount):
        if base not in currency:
            raise APIException(f'В списке валют нет "{base}"')
        if quote not in currency:
            raise APIException(f'В списке валют нет "{quote}"')
        if base == quote:
            raise APIException('Нет смысла переводить валюту в саму себя.')
        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Количество "{amount}" должно быть положительным числом.')
        if amount < 0:
            raise APIException(f'Количество "{amount}" должно быть положительным числом.')
        pair = f'{base}{quote}'
        params = dict(
            get='rates',
            pairs=pair,
            key=api_key
        )
        try:
            response = requests.get(url=api_url, params=params)
        except requests.ConnectionError:
            raise APIException(f'Сервер курсов валют не отвечает. Попробуйте отправить запрос позже.')
        price = response.json()['data'][pair]
        try:
            price = float(price)
        except ValueError:
            raise APIException(f'Сервер вернул не корректный курс валюты - "{price}".')
        return f'{amount} {base} ({currency[base]}) равно {amount * price} {quote} ({currency[quote]})'


######################################################################################################################
