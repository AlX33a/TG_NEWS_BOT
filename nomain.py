import telebot
from db_log import Database
from func import Tools
from keys import bot_token


#Initilizing
Database.start()
bot = telebot.TeleBot(bot_token)

def func1(message):
    global n
    user_id = message.chat.id

    if message.text == 'services':
        Tools.services(message)
        n = 1
    elif message.text == 'my news':
        Tools.my_news_message(message, user_id)
        n = 0
    elif message.text == 'set my news':
        Tools.news_set_first(message, user_id)
        n = 2

def func2(message):
    global n
    if message.text == '🌤 Погода 🌩':
        Tools.weather(message)
    elif message.text == '📰 Новости 📦':
        Tools.news(message)
    elif message.text == '💰 Крипто 🪙':
        Tools.cripto(message)
    elif message.text == '◀️':
            Tools.base_message(message)
            n = 0
    else:Tools.eror_message(message)

def func3(message):
    global n
    user_id = message.chat.id

    if message.text == '🌤 Погода 🌩 ➕':
        Database.any_update(user_id, 'weather', '1')
        Tools.news_set(message, user_id)
    elif message.text == '🌤 Погода 🌩 ✅':
        Database.any_update(user_id, 'weather', '0')
        Tools.news_set(message, user_id)
    elif message.text == '📰 Новости 📦 ➕':
        Database.any_update(user_id, 'news', '1')
        Tools.news_set(message, user_id)
    elif message.text == '📰 Новости 📦 ✅':
        Database.any_update(user_id, 'news', '0')
        Tools.news_set(message, user_id)
    elif message.text == '💰 Крипто 🪙 ➕':
        Database.any_update(user_id, 'cripto', '1')
        Tools.news_set(message, user_id)
    elif message.text == '💰 Крипто 🪙 ✅':
        Database.any_update(user_id, 'cripto', '0')
        Tools.news_set(message, user_id)
    elif message.text == '◀️':
            Tools.base_message(message)
            n = 0
    else:Tools.eror_message(message)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    if Database.user_check(user_id) == str(user_id):
        Tools.start_message(message) 
    else:
        Database.add_new_id(user_id)
        Tools.first_start_message(message)

@bot.message_handler(commands=['help'])
def help(message):
    Tools.help_message(message)

@bot.message_handler(content_types=['text'])
def answer(message):
    global n
    func1(message)

    if n == 1:
        func2(message)
    elif n == 2:
        func3(message)


if __name__ == '__main__':
    bot.infinity_polling()