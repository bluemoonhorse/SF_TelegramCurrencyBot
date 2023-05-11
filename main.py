import requests
import json
import pyTelegramBotAPI
import telebot

TOKEN = '6280326423:AAHL3px-D2_G0LsSHDSTCmLcBovZhEx9N74'
CRYPTO_API = '79056943495ea0828989d605d05b4cf61fe70dcdd99fb46805f5067d8663fc9d'
KEYS = {
    'BTC': 'BTC',
    'ETH': 'ETH',
    'USD': 'USD',
    'EUR': 'EUR',
    'XMR': 'XMR',
    'BYR': 'BYR',
}



bot = telebot.TeleBot(TOKEN)
guide_message = "Press /values to fetch list of tickers. " \
                "\n<ticker 1> <ticker 2> <1234>" \
                "\nBTC USD 1 = ????"

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Welcome, {message.chat.username}")
    bot.send_message(message.chat.id, guide_message)


@bot.message_handler(commands=['start', 'help'])
def get_help(message):
    bot.send_message(message.chat.id, guide_message)

@bot.message_handler(commands=['values'])
def get_values(message):
    text = "Тикеры доступных валют:"
    for key in KEYS.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    ###$$
    ticker1, ticker2, amount = message.text.split(" ")
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={KEYS[ticker1]}&tsyms={KEYS[ticker2]}&api_key={CRYPTO_API}')
    total_base = json.loads(r.content)[KEYS[ticker2]]

    text = f'Price of {amount} {ticker1} in {ticker2} : {total_base*float(amount)}'
    bot.reply_to(message, text)
    #альтернатива на будущее
    #r2 = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={ticker1}&tsyms={ticker2}&api_key={CRYPTO_API}')
    #text2 = json.loads(r2.content)[ticker2]
    #bot.reply_to(message, text2)





@bot.message_handler(content_types=['photo', ])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, 'Nice meme XDD')

# Обрабатываются все документы и аудиозаписи
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass


bot.polling(none_stop=True)