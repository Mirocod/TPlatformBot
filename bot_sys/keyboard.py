#-*-coding utf-8-*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

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

import math

def Chunks(a_List, a_ChunkSize):
    for i in range(0, len(a_List), a_ChunkSize):
        yield a_List[i: i + a_ChunkSize]

def MakeKeyboard(a_ButtonList : [ButtonWithAccess], a_UserGroups):
    buttons = []
    for b in a_ButtonList:
        if user_access.CheckAccessString(b.access_string, a_UserGroups, b.access_mode):
            buttons += [types.KeyboardButton(b.label)]
    step = max(int(math.sqrt(len(buttons)) // 1), 1)
    key = types.ReplyKeyboardMarkup(keyboard=Chunks(buttons, step), resize_keyboard = True)
    return key

def MakeKeyboardRemove():
    return types.ReplyKeyboardRemove()

def MakeKeyboardForMods(a_ModList, a_UserGroups):
    buttons = GetButtons(a_ModList)
    return MakeKeyboard(buttons, a_UserGroups)

class Button:
    def __init__(self, a_Label, a_CallBackData):
        self.label = a_Label
        self.callback_data = str(a_CallBackData)

def MakeInlineKeyboard(a_ButtonList : [Button], a_CallBackPrefix : str): 
    buttons = []
    for b in a_ButtonList:
        buttons += [types.InlineKeyboardButton(text = b.label, callback_data = f'{a_CallBackPrefix}{b.callback_data}')]
    step = max(int(math.sqrt(len(buttons)) // 1), 1)
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=Chunks(buttons, step))
    return inline_keyboard

