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
    chunk_list = []
    for i in range(0, len(a_List), a_ChunkSize):
         chunk_list += [a_List[i: i + a_ChunkSize]]
    return chunk_list

def GetButtonInRowCount(a_AllKeyCount):
    return min(max(int(math.sqrt(a_AllKeyCount) // 1), 1), 4)

def MakeAiogramKeyboard(a_ButtonList : [[str]]):
    return types.ReplyKeyboardMarkup(keyboard=a_ButtonList, resize_keyboard = True)

# TODO перенести KeyboardButton в MakeAiogramKeyboard
def MakeButtons(a_ButtonList : [ButtonWithAccess], a_UserGroups):
    buttons = []
    for b in a_ButtonList:
        if not b.label:
            continue
        if user_access.CheckAccessString(b.access_string, a_UserGroups, b.access_mode):
            buttons += [types.KeyboardButton(str(b.label))]
    step = GetButtonInRowCount(len(buttons))
    return Chunks(buttons, step)

def MakeKeyboard(a_ButtonList : [ButtonWithAccess], a_UserGroups):
    return MakeAiogramKeyboard(MakeButtons(a_ButtonList, a_UserGroups))

def MakeKeyboardRemove():
    return types.ReplyKeyboardRemove()

def MakeKeyboardForMods(a_ModList, a_UserGroups):
    buttons = GetButtons(a_ModList)
    return MakeKeyboard(buttons, a_UserGroups)

class InlineButton:
    def __init__(self, a_Label, a_CallBackData):
        self.label = a_Label
        self.callback_data = str(a_CallBackData)

class InlineButtonWithAccess:
    def __init__(self, a_Label, a_CallBackPrefix, a_CallBackData, a_AccessString, a_AccessMode):
        self.label = a_Label
        self.callback_prefix = a_CallBackPrefix
        self.callback_data = str(a_CallBackData)
        self.access_string = a_AccessString
        self.access_mode = a_AccessMode

def MakeAiogramInlineKeyboard(a_ButtonList : [InlineButton]): 
    buttons = []
    for row in a_ButtonList:
        r = []
        for b in row:
            r += [types.InlineKeyboardButton(text = str(b.label), callback_data = b.callback_data)]
        buttons += r
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_keyboard

def MakeInlineKeyboardButtons(a_ButtonList : [InlineButtonWithAccess], a_UserGroups): 
    buttons = []
    for b in a_ButtonList:
        if user_access.CheckAccessString(b.access_string, a_UserGroups, b.access_mode):
            buttons += [InlineButton(b.label, f'{b.callback_prefix}{b.callback_data}')]
    step = GetButtonInRowCount(len(buttons))
    return Chunks(buttons, step)

def MakeInlineKeyboard(a_ButtonList : [InlineButtonWithAccess], a_UserGroups): 
    return MakeAiogramInlineKeyboard(MakeInlineKeyboardButtons(a_ButtonList, a_UserGroups))
