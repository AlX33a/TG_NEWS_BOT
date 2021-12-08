import datetime
import requests

from pycoingecko import CoinGeckoAPI
from bs4 import BeautifulSoup
from keys import wet_key
from manager import bot


def time_converter(time):
    return datetime.datetime.fromtimestamp(time)

def weather(self):
    req = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q=Moscow&appid={wet_key}&units=metric"
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
    else:
        wd = "Неопределенно 😑\nОзнакомьтесь с данными ниже :3"

    temp = data['main']['temp']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    wind_speed = data['wind']['speed']
    sunrise = str(time_converter(data['sys']['sunrise']))[11:]
    sunset = str(time_converter(data['sys']['sunset']))[11:]
    daylight_hours = time_converter(data['sys']['sunset']) - time_converter(data['sys']['sunrise'])

    bot.reply_to(self,
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

def news(self):
    URL = 'https://ria.ru/world/'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    texts = soup.findAll('a', 'list-item__title')
    for i in range(len(texts[:5])):
        txt = f'{i + 1}) {texts[i].text}'
        bot.send_message(self.chat.id, f'<a href="{texts[i]["href"]}">{txt}</a>', parse_mode='html')

def cripto(message):
    api = CoinGeckoAPI()
    cript = api.get_price(ids=["bitcoin", "ethereum", "cardano", "solana", "polkadot"], vs_currencies="rub")
    bot.reply_to(message,
                 f'► {datetime.datetime.now().strftime("%Y/%m/%d %H:%M")} ◄\n'
                 f'💸 Курс криптовалют\n'
                 f'💶 Биткоин: {cript["bitcoin"]["rub"]} руб.\n'
                 f'💵 Эфириум: {cript["ethereum"]["rub"]} руб.\n'
                 f'💷 Solana: {cript["cardano"]["rub"]} руб.\n'
                 f'💵 Polkadot: {cript["solana"]["rub"]} руб.\n'
                 f'💴 Cardano: {cript["polkadot"]["rub"]} руб.\n'
                 )
