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

def GetButtonInRowCount(a_AllKeyCount):
    return min(max(int(math.sqrt(a_AllKeyCount) // 1), 1), 4)

def MakeKeyboard(a_ButtonList : [ButtonWithAccess], a_UserGroups):
    buttons = []
    for b in a_ButtonList:
        if user_access.CheckAccessString(b.access_string, a_UserGroups, b.access_mode):
            buttons += [types.KeyboardButton(b.label)]
    step = GetButtonInRowCount(len(buttons))
    key = types.ReplyKeyboardMarkup(keyboard=Chunks(buttons, step), resize_keyboard = True)
    return key

def MakeKeyboardRemove():
    return types.ReplyKeyboardRemove()

def MakeKeyboardForMods(a_ModList, a_UserGroups):
    buttons = GetButtons(a_ModList)
    return MakeKeyboard(buttons, a_UserGroups)

class InlineButton:
    def __init__(self, a_Label, a_CallBackPrefix, a_CallBackData, a_AccessString, a_AccessMode):
        self.label = a_Label
        self.callback_prefix = a_CallBackPrefix
        self.callback_data = str(a_CallBackData)
        self.access_string = a_AccessString
        self.access_mode = a_AccessMode

def MakeInlineKeyboard(a_ButtonList : [InlineButton], a_UserGroups): 
    buttons = []
    for b in a_ButtonList:
        if user_access.CheckAccessString(b.access_string, a_UserGroups, b.access_mode):
            buttons += [types.InlineKeyboardButton(text = b.label, callback_data = f'{b.callback_prefix}{b.callback_data}')]
    step = GetButtonInRowCount(len(buttons))
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=Chunks(buttons, step))
    return inline_keyboard

