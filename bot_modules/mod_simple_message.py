# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Простой модуль с одним сообщением

from bot_sys import keyboard, user_access
from bot_modules import access_utils, mod_interface
from template import simple_message, bd_item

from enum import Enum
from enum import auto

class ButtonNames(Enum):
    START = auto() 

class Messages(Enum):
    START = auto() 

class SimpleMessageModule(mod_interface.IModule):
    def __init__(self, a_Messages, a_Buttons, a_InitAccess, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_BotSubscribes, a_Log):
        self.m_ChildModuleNameList = a_ChildModuleNameList
        self.m_InitAccess = a_InitAccess
        self.m_Bot = a_Bot
        self.m_ModuleAgregator = a_ModuleAgregator
        self.m_BotMessages = a_BotMessages
        self.m_BotButtons = a_BotButtons
        self.m_BotSubscribes = a_BotSubscribes
        self.m_Log = a_Log

        self.m_Buttons = {}
        for name, button_name in a_Buttons.items():
            self.m_Buttons[name] = self.CreateButton(name, button_name)

        self.m_Messages = {}
        for name, message in a_Messages.items():
            self.m_Messages[name] = self.CreateMessage(name, message)

        async def StartMessageHandler(a_Message, state = None):
            return await self.StartMessageHandler(a_Message, state)
        self.m_StartMessageHandlerFunc = StartMessageHandler

        def GetAccess():
            return self.GetAccess()
        self.m_GetAccessFunc = GetAccess

        def GetStartKeyboardButtons(a_Message, a_UserGroups):
            return self.GetStartKeyboardButtons(a_Message, a_UserGroups)
        self.m_GetStartKeyboardButtonsFunc = GetStartKeyboardButtons

        self.m_StartMessageHandler = simple_message.SimpleMessageTemplate(
                self.m_Bot,
                self.m_StartMessageHandlerFunc,
                self.m_GetStartKeyboardButtonsFunc,
                None,
                self.m_GetAccessFunc
                )

    # Основной обработчик главного сообщения
    async def StartMessageHandler(self, a_Message, state = None):
        return simple_message.WorkFuncResult(self.GetMessage(Messages.START))

    def GetButton(self, a_ButtonName):
        return self.m_Buttons.get(a_ButtonName, None)

    def GetMessage(self, a_MessageNames):
        return self.m_Messages.get(a_MessageNames, None)

    def CreateMessage(self, a_MessageName, a_MessageDesc):
        msg = self.m_BotMessages.CreateMessage(f'{self.GetName()} {str(a_MessageName).replace("Messages.", "")}', a_MessageDesc, self.m_Log.GetTimeNow())
        return msg

    def CreateButton(self, a_ButtonName, a_ButtonDesc):
        if len(a_ButtonDesc) >= 41:
            print('ButtonDesc:', a_ButtonDesc)
            assert False # Телеграм не поддерживает больше
        assert a_ButtonDesc[0] != ' ' # Телеграм не поддерживает пробелы в начале
        assert a_ButtonDesc[-1:] != ' ' # Телеграм не поддерживает пробелы в конце
        # TODO добавить проверку, что все кнопки (a_ButtonDesc) разные
        btn = self.m_BotButtons.CreateMessage(f'{self.GetName()} {str(a_ButtonName).replace("ButtonNames.", "")}', a_ButtonDesc, self.m_Log.GetTimeNow())
        return btn

    def GetModule(self, a_ModName):
        return self.m_ModuleAgregator.GetModule(a_ModName)

    def GetButtons(self, a_ModNameList):
        buttons = []
        if not a_ModNameList:
            return buttons
        for n in a_ModNameList:
            m = self.m_ModuleAgregator.GetModule(n)
            b = m.GetModuleButtons()
            if not b is None or len(b) != 0:
                buttons += b
        return buttons

    def GetStartKeyboardButtons(self, a_Message, a_UserGroups):
        buttons = self.GetButtons(self.m_ChildModuleNameList)
        return keyboard.MakeButtons(self.m_Bot, buttons, a_UserGroups)

    def GetInitBDCommands(self):
        return [
                access_utils.GetAccessForModuleRequest(self.GetName(), self.m_InitAccess, self.m_InitAccess),
                ]

    def GetAccess(self):
        return access_utils.GetAccessForModule(self.m_Bot, self.GetName())

    def GetModuleButtons(self):
        return [
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.START), user_access.AccessMode.VIEW, self.GetAccess()),
                ]

    def RegisterHandlers(self):
        self.m_Bot.RegisterMessageHandler(
                self.m_StartMessageHandler, 
                bd_item.GetCheckForTextFunc(self.GetButton(ButtonNames.START))
                )

