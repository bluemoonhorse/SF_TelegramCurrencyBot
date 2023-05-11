import requests
import json
from config import KEYS, CRYPTO_API
class ConvertionException(Exception):
    pass


#Для отправки запросов к API описать класс со статическим методом get_price(),
#который принимает три аргумента: имя валюты, цену на которую надо узнать, — base, имя валюты,
#цену в которой надо узнать, — quote, количество переводимой валюты — amount и возвращает нужную сумму в валюте.+

# в скринкасте было лучше
class CryptoConverter(Exception):
    @staticmethod
    def get_price(base: str, quote: str, amount: float):
        # 🤔 работало и без keys[key] сразу на тикерах, ведь я сразу на тикерах делаю
        # пришлось заменить ticker1 & ticker2 на base & quote
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}&api_key={CRYPTO_API}')
        total_base = json.loads(r.content)[KEYS[quote]]
        # альтернатива на будущее
        # r2 = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym=
        # {base}&tsyms={quote}&api_key={CRYPTO_API}')
        # text2 = json.loads(r2.content)[quote]
        # bot.reply_to(message, text2)
        return total_base * float(amount)