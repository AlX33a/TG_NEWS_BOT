import telebot

import com_func
import db_log
import parser
from keys import bot_key

db_log.start()
bot = telebot.TeleBot(bot_key)
n = 0


# Команды
@bot.message_handler(commands=['start'])
def start(message):
    com_func.bot_start(message.chat.id, message)

@bot.message_handler(commands=['help'])
def help(message):
    com_func.help_message(message)

@bot.message_handler(content_types=['text'])
def answer(message):
    global n
    user_id = message.chat.id

    if n == 0:
        if message.text == 'services':
            com_func.services(message)
            n = 1
        elif message.text == 'my news':
            com_func.my_news_message(message, user_id)
        elif message.text == 'set my news':
            com_func.news_set_first(message, user_id)
            n = 2
        else:
            com_func.error_message(message)
    elif n == 1:
        if message.text == '🌤 Погода 🌩':
            parser.weather(message)
        elif message.text == '📰 Новости 📦':
            parser.news(message)
        elif message.text == '💰 Крипто 🪙':
            parser.cripto(message)
        elif message.text == '◀️':
            com_func.base_message(message)
            n = 0
        else:
            com_func.error_message(message)
    elif n == 2:
        if message.text == '🌤 Погода 🌩 ➕':
            db_log.any_update(user_id, 'weather', '1')
            com_func.news_set(message, user_id)
        elif message.text == '🌤 Погода 🌩 ✅':
            db_log.any_update(user_id, 'weather', '0')
            com_func.news_set(message, user_id)
        elif message.text == '📰 Новости 📦 ➕':
            db_log.any_update(user_id, 'news', '1')
            com_func.news_set(message, user_id)
        elif message.text == '📰 Новости 📦 ✅':
            db_log.any_update(user_id, 'news', '0')
            db_log.any_update(user_id, 'cripto', '1')
            com_func.news_set(message, user_id)
        elif message.text == '💰 Крипто 🪙 ✅':
            db_log.any_update(user_id, 'cripto', '0')
            com_func.news_set(message, user_id)
        elif message.text == '◀️':
            com_func.base_message(message)
            n = 0
        else:
            com_func.error_message(message)


if __name__ == '__main__':
    bot.infinity_polling()
