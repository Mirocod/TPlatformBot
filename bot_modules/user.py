# -*- coding: utf8 -*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 
from bot_sys import user_bd, log, config

from aiogram import types, Bot, Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token=config.GetTelegramBotApiToken(), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

# ---------------------------------------------------------
# Сообщения

start_message = '''
<b>👋 | Добро пожаловать!</b>

<b>Приятного пользования!</b>
'''

profile_message = '''
<b>Профиль:</b>

<b>ID:</b> @user_id
<b>Имя:</b> @user_name
'''

user_profile_button_name = "📰 Профиль"
back_to_start_menu_button_name = "◀  Назад"

# ---------------------------------------------------------
# Работа с кнопками

def GetStartKeyboardButtons():
    key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    prof_button = types.KeyboardButton(user_profile_button_name)
    key.add(prof_button)
    return key

def GetProfileKeyboardButtons():
    key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_to_start_menu = types.KeyboardButton(back_to_start_menu_button_name)
    key.add(back_to_start_menu)
    return key

# ---------------------------------------------------------
#

# Первичное привестивие
async def Welcome(a_Message):
    user_id = int(a_Message.from_user.id)
    user_name = str(a_Message.from_user.username)
    user_bd.AddUser(user_id, user_name)
    log.Info(f'Пользователь {user_id} {user_name} авторизовался в боте')
    await a_Message.answer(start_message, reply_markup=GetStartKeyboardButtons(), parse_mode='HTML')

# Отображение профиля пользователя
async def ProfileOpen(a_Message):
    user_id = str(a_Message.from_user.id)
    user_info = user_bd.GetUserInfo(user_id)
    msg = profile_message
    if not user_info is None:
        msg = msg.replace('@user_id', str(user_info[0])).replace('@user_name', str(user_info[1]))
    await bot.send_message(user_id, msg, reply_markup=GetProfileKeyboardButtons())

# Возврат в основное меню
async def BackToStartMunu(a_Message : types.Message):
    await Welcome(a_Message)

def RegisterHandlers(dp : Dispatcher):
    dp.register_message_handler(Welcome, commands=['start'])
    dp.register_message_handler(ProfileOpen, text=user_profile_button_name)
    dp.register_message_handler(BackToStartMunu, text=back_to_start_menu_button_name)


