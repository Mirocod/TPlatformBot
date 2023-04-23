#-*-coding utf-8-*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Работа с кнопками и клавиатурой

from aiogram import types, Bot, Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def GetButtons(a_ModList, a_UserAccess):
    names = []
    for m in a_ModList:
        n = m.GetButtonNames(a_UserAccess)
        if not n is None or len(n) != 0:
            names += n
    return names

def MakeKeyboard(a_ButtonList):
    key = types.ReplyKeyboardMarkup(resize_keyboard = True)
    for b in a_ButtonList:
        k = types.KeyboardButton(b)
        key.add(k)

    return key

def MakeKeyboardRemove():
    return types.ReplyKeyboardRemove()

def MakeKeyboardForMods(a_ModList, a_UserAccess):
    names = GetButtons(a_ModList, a_UserAccess)
    return MakeKeyboard(names)
    buttons = GetButtons(a_ModList, a_UserAccess)
    return MakeKeyboard(buttons)

class Button:
    def __init__(self, a_Label, a_CallBackData):
        self.label = a_Label
        self.callback_data = a_CallBackData

def MakeInlineKeyboard(a_ButtonList, a_CallBackPrefix): # class Button
    inline_keyboard = InlineKeyboardMarkup()
    for b in a_ButtonList:
        inline_keyboard.insert(types.InlineKeyboardButton(text = b.label, callback_data = f'{a_CallBackPrefix}{b.callback_data}'))
    return inline_keyboard

