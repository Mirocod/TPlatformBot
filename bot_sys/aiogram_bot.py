#-*-coding utf-8-*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

from bot_sys import interfaces, bot_bd, keyboard

from aiogram import types
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

class AiogramBot(interfaces.IBot):
    def __init__(self, a_TelegramBotApiToken, a_BDFileName, a_RootIDs, a_Log):
        self.m_TelegramBotApiToken = a_TelegramBotApiToken
        self.m_BDFileName = a_BDFileName
        self.m_RootIDs = a_RootIDs
        self.m_Log = a_Log
        self.m_TBot = Bot(token=self.m_TelegramBotApiToken, parse_mode = types.ParseMode.HTML)
        self.m_Storage = MemoryStorage()
        self.m_Dispatcher = Dispatcher(self.m_TBot, storage = storage)

    def GetRootIDs():
        return self.m_RootIDs

    def GetLog():
        return self.m_Log

    def SQLRequest(self, a_Request : str, commit = False, return_error = False, param = None):
        return bot_bd.SQLRequest(self.m_BDFileName, a_Request, commit = commit, return_error = return_error, param = param)

    def GetUserGroupData(a_UserID):
        def GetGroupNamesForUser(a_UserID):
            return SQLRequest('SELECT groupName FROM user_groups WHERE group_id=(SELECT group_id FROM user_in_groups WHERE user_id = ?)', param = [a_UserID])
        r = GetGroupNamesForUser(a_UserID)
        groups = []
        for i in r:
            if len(i) > 0:
                groups += [i[0]]
        return user_access.UserGroups(a_UserID, groups)

    def GetModulesAccessList():
        return bot_bd.RequestSelectTemplate(self.m_BDFileName, table_name)()

    def GetAccessForModule(a_ModuleName):
        alist = GetModulesAccessList()
        for i in alist:
            if i[0] == a_ModuleName:
                return i[1]
        return ''

    def GetItemDefaultAccessForModule(a_ModuleName):
        alist = GetModulesAccessList()
        for i in alist:
            if i[0] == a_ModuleName:
                return i[2]
        return ''

    async def SendMessage(self, a_UserID, a_Message, a_PhotoIDs, a_InlineKeyboardButtons, a_KeyboardButtons):
        inline_keyboard = keyboard.MakeAiogramInlineKeyboard(a_InlineKeyboardButtons)
        keyboard = keyboard.MakeAiogramKeyboard(a_KeyboardButtons)
        if not keyboard:
                keyboard = inline_keyboard
        if a_PhotoIDs and a_PhotoIDs != 0 or a_PhotoIDs != '0':
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

