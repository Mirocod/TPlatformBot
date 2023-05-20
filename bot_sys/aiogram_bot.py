#-*-coding utf-8-*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

from bot_sys import interfaces, bot_bd, keyboard, user_access

from aiogram import types
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

def MakeAiogramInlineKeyboards(a_ButtonList : [InlineButton]): 
    buttons = []
    for row in a_ButtonList:
        r = []
        for b in row:
            r += [types.InlineKeyboardButton(text = str(b.label), callback_data = b.callback_data)]
        buttons += [r]

    button_list_chunks = keyboard.Chunks(buttons, 20)
    result = []
    for c in button_list_chunks:
        result += [InlineKeyboardMarkup(inline_keyboard=c)]

    return result

def MakeAiogramKeyboard(a_ButtonList : [[str]]):
    return types.ReplyKeyboardMarkup(keyboard=a_ButtonList, resize_keyboard = True)

class AiogramBot(interfaces.IBot):
    def __init__(self, a_TelegramBotApiToken, a_BDFileName, a_RootIDs, a_Log):
        self.m_TelegramBotApiToken = a_TelegramBotApiToken
        self.m_BDFileName = a_BDFileName
        self.m_RootIDs = a_RootIDs
        self.m_Log = a_Log
        self.m_TBot = Bot(token=self.m_TelegramBotApiToken, parse_mode = types.ParseMode.HTML)
        self.m_Storage = MemoryStorage()
        self.m_Dispatcher = Dispatcher(self.m_TBot, storage = self.m_Storage)

    def GetRootIDs(self):
        return self.m_RootIDs

    def GetLog(self):
        return self.m_Log

    def SQLRequest(self, a_Request : str, commit = False, return_error = False, param = None):
        return bot_bd.SQLRequest(self.m_BDFileName, a_Request, commit = commit, return_error = return_error, param = param)

    async def SendMessage(self, a_UserID, a_Message, a_PhotoIDs, a_KeyboardButtons, a_InlineKeyboardButtons, parse_mode = None):
        if not parse_mode:
            parse_mode = types.ParseMode.HTML
        inline_keyboards = None
        if a_InlineKeyboardButtons:
            inline_keyboards = keyboard.MakeAiogramInlineKeyboards(a_InlineKeyboardButtons)
        base_keyboards = None
        if a_KeyboardButtons:
            base_keyboards = [keyboard.MakeAiogramKeyboard(a_KeyboardButtons)]
        if inline_keyboards:
                base_keyboards = inline_keyboards
        if a_PhotoIDs and a_PhotoIDs != 0 and a_PhotoIDs != '0':
            for k in base_keyboards:
                await self.m_TBot.send_photo(
                        a_UserID,
                        a_PhotoIDs,
                        a_Message,
                        reply_markup = k
                        )
        else:
            #print('SendMessage', a_UserID, a_Message, a_PhotoIDs, a_InlineKeyboardButtons, a_KeyboardButtons, base_keyboard)
            for k in base_keyboards:
                await self.m_TBot.send_message(
                        a_UserID,
                        a_Message,
                        reply_markup = k,
                        parse_mode = parse_mode
                        )

    async def SendDocument(self, a_UserID, a_Document, a_Caption, a_KeyboardButtons, a_InlineKeyboardButtons):
        inline_keyboard = None
        if a_InlineKeyboardButtons:
            inline_keyboard = keyboard.MakeAiogramInlineKeyboard(a_InlineKeyboardButtons)
        base_keyboard = None
        if a_KeyboardButtons:
            base_keyboard = keyboard.MakeAiogramKeyboard(a_KeyboardButtons)
        if inline_keyboard:
                base_keyboard = inline_keyboard
        await self.m_TBot.send_document(
                        a_UserID,
                        a_Document,
                        caption = a_Caption,
                        reply_markup = base_keyboard
                        )

    def RegisterMessageHandler(self, a_MessageHandler, a_CheckFunc=None, commands=None, regexp=None, content_types=None, state=None):
        if a_CheckFunc:
            self.m_Dispatcher.register_message_handler(a_MessageHandler, a_CheckFunc, commands=commands, regexp=regexp, content_types=content_types, state=state)
        else:
            self.m_Dispatcher.register_message_handler(a_MessageHandler, commands=commands, regexp=regexp, content_types=content_types, state=state)

    def RegisterCallbackHandler(self, a_CallbackHandler, a_CheckFunc=None, commands=None, regexp=None, content_types=None, state=None):
        if a_CheckFunc:
            self.m_Dispatcher.register_callback_query_handler(a_CallbackHandler, a_CheckFunc, commands=commands, regexp=regexp, content_types=content_types, state=state)
        else:
            self.m_Dispatcher.register_callback_query_handler(a_CallbackHandler, commands=commands, regexp=regexp, content_types=content_types, state=state)

    def StartPolling(self):
        executor.start_polling(self.m_Dispatcher)

