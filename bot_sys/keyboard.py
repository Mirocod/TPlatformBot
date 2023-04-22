#-*-coding utf-8-*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Работа с кнопками и клавиатурой

from aiogram import types, Bot, Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def MakeKeyboard(a_ButtonList):
    key = types.ReplyKeyboardMarkup(resize_keyboard = True)
    for b in a_ButtonList:
        k = types.KeyboardButton(b)
        key.add(k)

    return key
