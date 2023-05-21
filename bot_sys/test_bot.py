#-*-coding utf-8-*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

from bot_sys import interfaces, bot_bd, keyboard, user_access, test_log

import asyncio

class UserData():
    def __init__(self, a_id, a_username, a_first_name, a_last_name, a_is_bot, a_language_code):
        self.id = a_id
        self.username = a_username
        self.first_name = a_first_name
        self.last_name = a_last_name
        self.is_bot = a_is_bot
        self.language_code = a_language_code

class UserPhoto():
    def __init__(self, a_PhotoID):
        self.file_id = a_PhotoID

class UserMessage():
    def __init__(self, a_UserData, a_Message, a_PhotoID):
        self.from_user = a_UserData
        self.text = a_Message
        if not a_PhotoID:
            self.photo = None
        self.photo = [UserPhoto(a_PhotoID)]

class BotMessage():
    def __init__(self, a_Message, a_PhotoIDs, a_KeyboardButtons, a_InlineKeyboardButtons, parse_mode = None):
        self.m_Message = a_Message
        self.m_PhotoIDs = a_PhotoIDs
        self.m_KeyboardButtons = a_KeyboardButtons
        self.m_InlineKeyboardButtons = a_InlineKeyboardButtons
        self.m_parse_mode = parse_mode

class BotMessageHandler():
    def __init__(self, a_MessageHandler, a_CheckFunc=None, commands=None, regexp=None, content_types=None, state=None):
        self.m_MessageHandler = a_MessageHandler
        self.m_CheckFunc = a_CheckFunc
        self.m_commands = commands
        self.m_regexp = regexp
        self.m_content_types = content_types
        self.m_state = state

class TestBot(interfaces.IBot):
    def __init__(self, a_BDFileName, a_RootIDs, a_Log):
        self.m_BDFileName = a_BDFileName
        self.m_RootIDs = a_RootIDs
        self.m_Log = a_Log
        self.m_UserMessage = {}
        self.m_BotMessage = {}
        self.m_BotMessageHandlers = []

    def SendUserMessage(self, a_UserData : UserData, a_Message, a_PhotoIDs):
        user_id = a_UserData.id
        if not self.m_UserMessage.get(user_id, None):
            self.m_UserMessage[user_id] = []
        self.m_UserMessage[user_id] += [UserMessage(a_UserData, a_Message, a_PhotoIDs)]

    def GetBotMessage(self, a_UserID): # return [BotMessage]
        result = self.m_BotMessage.get(a_UserID, None)
        self.m_BotMessage[a_UserID] = []
        return result

    def GetRootIDs(self):
        return self.m_RootIDs

    def GetLog(self):
        return self.m_Log

    def SQLRequest(self, a_Request : str, commit = False, return_error = False, param = None):
        return bot_bd.SQLRequest(self.m_Log, self.m_BDFileName, a_Request, commit = commit, return_error = return_error, param = param)

    async def SendMessage(self, a_UserID, a_Message, a_PhotoIDs, a_KeyboardButtons, a_InlineKeyboardButtons, parse_mode = None):
        self.m_BotMessage[a_UserID] = [BotMessage(a_Message, a_PhotoIDs, a_KeyboardButtons, a_InlineKeyboardButtons, parse_mode = parse_mode)]

    async def SendDocument(self, a_UserID, a_Document, a_Caption, a_KeyboardButtons, a_InlineKeyboardButtons):
        pass

    def RegisterMessageHandler(self, a_MessageHandler, a_CheckFunc=None, commands=None, regexp=None, content_types=None, state=None):
        self.m_BotMessageHandlers += [BotMessageHandler(a_MessageHandler, a_CheckFunc=a_CheckFunc, commands=commands, regexp=regexp, content_types=content_types, state=state)]

    def RegisterCallbackHandler(self, a_CallbackHandler, a_CheckFunc=None, commands=None, regexp=None, content_types=None, state=None):
        pass

    def StartPolling(self):
        for user_id, user_msgs in self.m_UserMessage.items():
            for user_msg in user_msgs:
                for message_handler in self.m_BotMessageHandlers:
                    check = False
                    if message_handler.m_CheckFunc:
                        check = m_CheckFunc(user_msg)
                    cmds = message_handler.m_commands
                    if cmds:
                        for c in cmds:
                            if '/'+ c == user_msg.text:
                                check = True
                            print('user_msg.text', user_msg.text, c, check)
                    # TODO : добавить обработку regexp content_types state
                    if check:
                        print('message_handler', message_handler.m_MessageHandler, user_msg)
                        asyncio.run(message_handler.m_MessageHandler(user_msg, state = message_handler.m_state))
        self.m_UserMessage = {}

def Test():
    print('Test')
    log = test_log.TestLog()
    root_id = '234353425'
    a_RootIDs = [root_id]
    a_BDFileName = 'test_bd.bd'
    bot = TestBot(a_BDFileName, a_RootIDs, log)

    user_kb = [['user_kb']]
    user_ikb = [['user_ikb']]
    user_parse_mode = 'html'
    async def TestMessageHandler(a_Message, state = None):
        user_id = str(a_Message.from_user.id)
        print('user_id', user_id)
        await bot.SendMessage(user_id, a_Message.text, a_Message.photo[0].file_id, user_kb, user_ikb, user_parse_mode)

    bot.RegisterMessageHandler(TestMessageHandler, commands = ['start'])
    user_photo_id = '435456567'
    user_message = '/start'

    user_data = UserData(root_id, 'a_username', 'a_first_name', 'a_last_name', 'False', 'ru')
    bot.SendUserMessage(user_data, user_message, user_photo_id)

    bot.StartPolling()

    bot_messages = bot.GetBotMessage(root_id)

    assert len(bot_messages) == 1
    bot_message = bot_messages[0]

    assert bot_message.m_Message == user_message
    assert bot_message.m_PhotoIDs == user_photo_id
    assert bot_message.m_KeyboardButtons[0][0] == user_kb[0][0]
    assert bot_message.m_InlineKeyboardButtons[0][0] == user_ikb[0][0]
    assert bot_message.m_parse_mode == user_parse_mode

