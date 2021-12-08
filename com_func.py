from telebot import types

import db_log
import parser
from manager import bot


# Действия команд
def bot_start(user_id, mes):
    if db_log.user_check(user_id) == str(user_id):
        start_message(mes)
    else:
        db_log.add_new_id(user_id)
        first_start_message(mes)
def help_message(mes):
    markup = first_panel()
    bot.send_message(mes.chat.id, f'''У меня ты можешь: настроить свои новости в разделе set my news и получать их по кнопке my news, изначально по этой кнопке ты получишь все доступные новости. Также по кнопке services ты можешь посмотреть новости по разделам.
    ''', reply_markup=markup)

# Ответы
def start_message(mes):
    markup = first_panel()
    bot.send_message(mes.chat.id, f"""И тебе доброго времени суток, любитель новостей!\nЕсли забыл про мои возможности пиши /help
    """, reply_markup=markup)
def first_start_message(mes):
    markup = first_panel()
    bot.send_message(mes.chat.id, f"""Привет!\nЯ вижу ты новенький.\nМеня зовут Miig bot!\nСоветую тебе ознакомится с моими возможностями при помощи /help
    """, reply_markup=markup)
def services(mes):
    markup = second_panel()
    bot.send_message(mes.chat.id, 'Здесь все сервисы новостей.', reply_markup=markup)
def my_news_message(mes, user_id):
    k = 0
    if db_log.service_check(user_id)[0:1] == '1':
        parser.weather(mes)
        k += 1
    if db_log.service_check(user_id)[1:2] == '1':
        parser.news(mes)
        k += 1
    if db_log.service_check(user_id)[2:3] == '1':
        parser.cripto(mes)
        k += 1
    else:
        if k == 0:
            bot.send_message(mes.chat.id, 'Вы не выбрали ни одного сервиса :(')
        else:
            pass
def news_set_first(mes, user_id):
    markup = set_panel(user_id)
    bot.send_message(mes.chat.id, 'Какие новости вы хотите видеть в разделе my news.', reply_markup=markup)
def error_message(mes):
    bot.send_message(mes.chat.id, 'Выберите кнопку на панели.')
def base_message(mes):
    markup = first_panel()
    bot.send_message(mes.chat.id, f'''Выбери нужную кнопку.
    ''', reply_markup=markup)
def news_set(mes, user_id):
    markup = set_panel(user_id)
    bot.send_message(mes.chat.id, 'Сделано, что-то еще?', reply_markup=markup)

# Кнопки
def first_panel():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    m1 = types.KeyboardButton('set my news')
    m2 = types.KeyboardButton('my news')
    m3 = types.KeyboardButton('services')
    return markup.add(m1, m2, m3)
def second_panel():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    m5 = types.KeyboardButton('🌤 Погода 🌩')
    m6 = types.KeyboardButton('📰 Новости 📦')
    m7 = types.KeyboardButton('💰 Крипто 🪙')
    m8 = types.KeyboardButton('◀️')
    return markup.add(m5, m6, m7, m8)

# Панель
def set_panel(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if db_log.service_check(user_id)[0:1] == '1':
        m9 = types.KeyboardButton('🌤 Погода 🌩 ✅')
    else:
        m9 = types.KeyboardButton('🌤 Погода 🌩 ➕')
    if db_log.service_check(user_id)[1:2] == '1':
        m10 = types.KeyboardButton('📰 Новости 📦 ✅')
    else:
        m10 = types.KeyboardButton('📰 Новости 📦 ➕')
    if db_log.service_check(user_id)[2:3] == '1':
        m11 = types.KeyboardButton('💰 Крипто 🪙 ✅')
    else:
        m11 = types.KeyboardButton('💰 Крипто 🪙 ➕')
    m12 = types.KeyboardButton('◀️')
    return markup.add(m9, m10, m11, m12)
