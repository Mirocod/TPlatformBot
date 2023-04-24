#-*-coding utf-8-*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Работа с кнопками и клавиатурой

from bot_sys import user_access
from aiogram import types, Bot, Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

class ButtonWithAccess:
    def __init__(self, a_Label, a_AccessMode : user_access.AccessMode, a_AccessString):
        self.label = a_Label
        self.access_mode = a_AccessMode
        self.access_string = a_AccessString

def GetButtons(a_ModList):
    buttons = []
    for m in a_ModList:
        b = m.GetModuleButtons()
        if not b is None or len(b) != 0:
            buttons += b
    return buttons

def MakeKeyboard(a_ButtonList : [ButtonWithAccess], a_UserGroups):
    key = types.ReplyKeyboardMarkup(resize_keyboard = True)
    for b in a_ButtonList:
        if user_access.CheckAccessString(b.access_string, a_UserGroups, b.access_mode):
            k = types.KeyboardButton(b.label)
            key.add(k)

    return key

def MakeKeyboardRemove():
    return types.ReplyKeyboardRemove()

def MakeKeyboardForMods(a_ModList, a_UserGroups):
    buttons = GetButtons(a_ModList)
    return MakeKeyboard(buttons, a_UserGroups)

class Button:
    def __init__(self, a_Label, a_CallBackData):
        self.label = a_Label
        self.callback_data = a_CallBackData

def MakeInlineKeyboard(a_ButtonList, a_CallBackPrefix): # class Button
    inline_keyboard = InlineKeyboardMarkup()
    for b in a_ButtonList:
        inline_keyboard.insert(types.InlineKeyboardButton(text = b.label, callback_data = f'{a_CallBackPrefix}{b.callback_data}'))
    return inline_keyboard

