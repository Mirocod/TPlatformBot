# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Профиль пользователя

from bot_sys import bot_bd, log, config, keyboard
from bot_modules import start
from aiogram import Bot, types

import sqlite3

from aiogram.dispatcher import Dispatcher

bot = Bot(token=config.GetTelegramBotApiToken(), parse_mode=types.ParseMode.HTML)

# ---------------------------------------------------------
# БД
init_bd_cmd = """CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER,
    userName TEXT,
    UNIQUE(user_id)
);"""

# ---------------------------------------------------------
# Сообщения

profile_message = '''
<b>Профиль:</b>

<b>ID:</b> @user_id
<b>Имя:</b> @user_name
'''

user_profile_button_name = "📰 Профиль"

# ---------------------------------------------------------
# Работа с кнопками

def GetProfileKeyboardButtons(a_UserAccess):
    start_button_names = start.GetButtonNames(a_UserAccess)
    return keyboard.MakeKeyboard([start_button_names])

# ---------------------------------------------------------
# Обработка сообщений

# Отображение профиля пользователя
async def ProfileOpen(a_Message):
    user_id = str(a_Message.from_user.id)
    user_info = GetUserInfo(user_id)
    msg = profile_message
    if not user_info is None:
        msg = msg.replace('@user_id', str(user_info[0])).replace('@user_name', str(user_info[1]))
    await bot.send_message(user_id, msg, reply_markup = GetProfileKeyboardButtons(None))

# ---------------------------------------------------------
# Работа с базой данных пользователей

# Добавление пользователя, если он уже есть, то игнорируем
def AddUser(a_UserID, a_UserName):
    db = sqlite3.connect(bot_bd.GetBDFileName())
    cursor = db.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, userName) VALUES (?, ?);", (a_UserID, a_UserName));
    db.commit()
    cursor.close()
    db.close()

# Добавление пользователя, если он уже есть, то игнорируем
def GetUserInfo(a_UserID):
    db = sqlite3.connect(bot_bd.GetBDFileName())
    cursor = db.cursor()
    user_info = cursor.execute('SELECT * FROM users WHERE user_id = ?', ([a_UserID])).fetchall()
    cursor.close()
    db.close()
    if len(user_info) != 0:
        return user_info[0]
    return None

# ---------------------------------------------------------
# API

# Доступные кнопки
def GetInitBDCommands():
    return [init_bd_cmd]

# Доступные кнопки
def GetButtonNames(a_UserAccess):
    return user_profile_button_name

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    dp.register_message_handler(ProfileOpen, text = user_profile_button_name)
