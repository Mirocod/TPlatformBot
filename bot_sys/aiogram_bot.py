#-*-coding utf-8-*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

from bot_sys import interfaces, bot_bd, keyboard

from aiogram import types
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

class AiogramBot(IBot):
    def __init__(self, a_TelegramBotApiToken, a_BDFileName):
        self.m_TelegramBotApiToken = a_TelegramBotApiToken
        self.m_BDFileName = a_BDFileName
        self.m_TBot = Bot(token=self.m_TelegramBotApiToken, parse_mode = types.ParseMode.HTML)
        self.m_Storage = MemoryStorage()
        self.m_Dispatcher = Dispatcher(self.m_TBot, storage = storage)

    def SQLRequest(self, a_Request : str, commit = False, return_error = False, param = None):
        return bot_bd.SQLRequest(self.m_BDFileName, a_Request, commit = commit, return_error = return_error, param = param)

    async def SendMessage(self, a_UserID, a_Message, a_PhotoIDs, a_InlineKeyboardButtons, a_KeyboardButtons):
        inline_keyboard = keyboard.MakeAiogramInlineKeyboard(a_InlineKeyboardButtons)
        keyboard = keyboard.MakeAiogramKeyboard(a_KeyboardButtons)
        if not keyboard:
                keyboard = inline_keyboard
        if a_PhotoIDs:
                self.m_TBot.send_photo(
                        a_UserID,
                        a_PhotoIDs,
                        a_Message,
                        reply_markup = keyboard
                        )
        else:
                self.m_TBot.send_message(
                        a_UserID,
                        a_Message,
                        reply_markup = keyboard
                        )

    def RegisterMessageHandler(self, a_MessageHandler, a_CheckFunc):
       self.m_Dispatcher.register_message_handler(a_MessageHandler, a_CheckFunc)

    def RegisterCallbackHandler(self, a_CallbackHandler, a_CheckFunc):
       self.m_Dispatcher.register_callback_query_handler(a_CallbackHandler, a_CheckFunc)

