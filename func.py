from db_log import Database
import telebot
import datetime
import requests
from bs4 import BeautifulSoup
from keys import bot_token, WET_KEY
from telebot import types

#Initilizing
bot = telebot.TeleBot(bot_token)

class Tools:
    global n


    def first_panel(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        m1 = types.KeyboardButton('set my news')
        m2 = types.KeyboardButton('my news')
        m3 = types.KeyboardButton('services')
        return markup.add(m1, m2, m3)

    def second_panel(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        m5 = types.KeyboardButton('🌤 Погода 🌩')
        m6 = types.KeyboardButton('📰 Новости 📦')
        m7 = types.KeyboardButton('💰 Крипто 🪙')
        m8 = types.KeyboardButton('◀️')
        return markup.add(m5, m6, m7, m8)

    def set_panel(message, user_id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if Database.service_check(user_id)[0:1] == '1':
            m9 = types.KeyboardButton('🌤 Погода 🌩 ✅')
        else: m9 = types.KeyboardButton('🌤 Погода 🌩 ➕')
        if Database.service_check(user_id)[1:2] == '1':
            m10 = types.KeyboardButton('📰 Новости 📦 ✅')
        else: m10 = types.KeyboardButton('📰 Новости 📦 ➕')
        if Database.service_check(user_id)[2:3] == '1':
            m11 = types.KeyboardButton('💰 Крипто 🪙 ✅')
        else: m11 = types.KeyboardButton('💰 Крипто 🪙 ➕')
        m12 = types.KeyboardButton('◀️')
        return markup.add(m9, m10, m11, m12)

    def news_set_first(message, user_id):
        markup = Tools.set_panel(message, user_id)
        bot.send_message(message.chat.id, 'Какие новости вы хотите видеть в разделе my news.', reply_markup=markup)

    def news_set(message, user_id):
        markup = Tools.set_panel(message, user_id)
        bot.send_message(message.chat.id, 'Сделано, что-то еще?', reply_markup=markup)

    def first_start_message(message):
        markup = Tools.first_panel(message)
        bot.send_message(message.chat.id, f'''Привет!\nЯ вижу ты новенький.\nМеня зовут Miig bot!\nСоветую тебе ознакомится с моими возможностями при помощи /help 
        ''', reply_markup=markup)

    def help_message(message):
        markup = Tools.first_panel(message)
        bot.send_message(message.chat.id, f'''У меня ты можешь: настроить свои новости в разделе set my news и получать их по кнопке my news, изначально по этой кнопке ты получишь все доступные новости. Также по кнопке services ты можешь посмотреть новости по разделам.
        ''', reply_markup=markup)

    def start_message(message):
        markup = Tools.first_panel(message)
        bot.send_message(message.chat.id, f'''И тебе доброго времени суток, любитель новостей!\nЕсли забыл про мои возможности пиши /help
        ''', reply_markup=markup)

    def base_message(message):
        markup = Tools.first_panel(message)
        bot.send_message(message.chat.id, f'''Выбери нужную кнопку.
        ''', reply_markup=markup)

    def services(message):
        markup = Tools.second_panel(message)
        bot.send_message(message.chat.id,'Здесь все сервисы новостей.', reply_markup=markup)

    def time_converter(time):
            return datetime.datetime.fromtimestamp(time)

    def my_news_message(message, user_id):
        k = 0
        if Database.service_check(user_id)[0:1] == '1':
            Tools.weather(message)
            k  += 1
        if Database.service_check(user_id)[1:2] == '1':
            Tools.news(message)
            k += 1
        if Database.service_check(user_id)[2:3] == '1':
            Tools.cripto(message)
            k += 1
        else: 
            if k == 0 : bot.send_message(message.chat.id,'Вы не выбрали ни одного сервиса :(')
            else: pass

    def eror_message(message):
        bot.send_message(message.chat.id,'Выберите кнопку на панели.')

    def weather(message):
        req = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q=Moscow&appid={WET_KEY}&units=metric"
        )
        data = req.json()
        code_to_smile = {
            "Clear": "Ясно ☀",
            "Clouds": "Облачно ☁",
            "Rain": "Дождь ☔",
            "Drizzle": "Дождь ☔",
            "Thunderstorm": "Гроза ⚡",
            "Snow": "Снег 🌨",
            "Mist": "Туман 🌫"
        }
        weather_description = data["weather"][0]["main"]

        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else: wd = "Неопределено 😑\nОзнакомьтесь с данными ниже :3"

        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        sunrise = str(Tools.time_converter(data['sys']['sunrise']))[11:]
        sunset = str(Tools.time_converter(data['sys']['sunset']))[11:]
        daylight_hours = Tools.time_converter(data['sys']['sunset']) - Tools.time_converter(data['sys']['sunrise'])

        bot.reply_to(message,
                     f'► {datetime.datetime.now().strftime("%Y/%m/%d %H:%M")} ◄\n'
                     f'🌀 Погода в Москве сейчас: {wd}\n'
                     f'🌡️ Температра: {temp}С°\n'
                     f'💦 Влажность: {humidity}%\n'
                     f'💪 Давление: {pressure} мм. рт. ст.\n'
                     f'🚀 Скорость ветра: {wind_speed} м/с\n'
                     f'🌚 Время рассвета: {sunrise}\n'
                     f'🌝 Время заката: {sunset}\n'
                     f'🕒 Продолжительность дня: {daylight_hours}\n'
                     )

    def news(message):
        URL = 'https://ria.ru/world/'
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}
        response = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.findAll('a', 'list-item__title')
        for i in range(len(texts[:5])):
            txt = f'{i + 1}) {texts[i].text}'
            bot.send_message(message.chat.id, f'<a href="{texts[i]["href"]}">{txt}</a>', parse_mode='html')
    
    def cripto(message):
        cript = {'BTC': 0, 'ETH': 0, 'ADA': 0, 'SOL': 0, 'DOT': 0}
        for i in cript:
            request = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={i}&tsyms={"RUB"}')
            data = request.json()
            cript[i] = data['RUB']
        bot.reply_to(message,
                     f'► {datetime.datetime.now().strftime("%Y/%m/%d %H:%M")} ◄\n'
                     f'💸 Курс криптовалют\n'
                     f'💶 Биткоин: {cript["BTC"]} руб.\n'
                     f'💵 Эфириум: {cript["ETH"]} руб.\n'
                     f'💷 Solana: {cript["SOL"]} руб.\n'
                     f'💵 Polkadot: {cript["DOT"]} руб.\n'
                     f'💴 Cardano: {cript["ADA"]} руб.\n'
                     )