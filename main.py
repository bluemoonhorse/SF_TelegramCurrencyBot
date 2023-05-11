import pyTelegramBotAPI
from pyTelegramBotAPI import telebot
from extensions import ConvertionException, CryptoConverter
from config import TOKEN, KEYS




bot = telebot.TeleBot(TOKEN)
guide_message = "Press /values to fetch list of tickers. " \
                "\n<ticker 1> <ticker 2> <1234>" \
                "\nBTC USD 1 = ????"


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.


@bot.message_handler(commands=['start', 'help'])
def get_help(message):
    bot.send_message(message.chat.id, guide_message)


@bot.message_handler(commands=['values'])
def get_values(message):
    text = "Тикеры доступных валют:"
    for key in KEYS.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

#Для отправки запросов к API описать класс со статическим методом get_price(),
#который принимает три аргумента: имя валюты, цену на которую надо узнать, — base, имя валюты,
#цену в которой надо узнать, — quote, количество переводимой валюты — amount и возвращает нужную сумму в валюте.+



@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(" ")

    if len(values) != 3:
        bot.reply_to(message, "I need 3 parameters")
        raise ConvertionException("I need 3 parameters")

    base, quote, amount = values

    if float(amount) <= 0:
        # подскажите как захватывать error message в try-except-raise("say stuff") через класс  😭😭😭😭😭
        bot.reply_to(message, "Number should be positive!")
        raise ConvertionException("Number should be positive!")
    if base == quote:
        # 1 xmr = 1 xmr! 🍊
        bot.reply_to(message, "1 XMR = 1 XMR! Those are the same currencies!")
        raise ConvertionException("1 XMR = 1 XMR! Those are the same currencies!")
    try:
        base = KEYS[base]
    except KeyError:
        bot.reply_to(message, f'Currency check has failed: {base}')
        raise ConvertionException(f'Currency check has failed: {base}')
    try:
        quote = KEYS[quote]
    except KeyError:
        bot.reply_to(message, f'Currency check has failed: {quote}')
        raise ConvertionException(f'Currency check has failed: {quote}')
    try:
        amount = float(amount)
    except ValueError:
        bot.reply_to(message, f'I need number: {amount}')
        raise ConvertionException(f'I need number: {amount}')

    total_base = CryptoConverter.get_price(base, quote, amount)
    text = f'Price of {amount} {base} in {quote} : {total_base}'
    bot.reply_to(message, text)
    # альтернатива на будущее оказалась не альтернативой
    # r2 = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}&api_key={CRYPTO_API}')
    # text2 = json.loads(r2.content)[quote]
    # bot.reply_to(message, text2)


#наследство скилфактори но пригодилось
@bot.message_handler(content_types=['photo', 'document', 'audio'])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, 'https://www.getmonero.org')


# bot.polling(none_stop=True)
bot.infinity_polling()
