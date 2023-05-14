# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Простой модуль с одним сообщением

from bot_sys import keyboard, user_access, keyboard
from bot_modules import access, mod_interface
from template import simple_message, bd_item

class SimpleMessageModule(mod_interface.IModule):
    def __init__(self, a_StartMessage, a_StartButtonName, a_InitAccess, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        self.m_ChildModuleNameList = a_ChildModuleNameList
        self.m_InitAccess = a_InitAccess
        self.m_Bot = a_Bot
        self.m_ModuleAgregator = a_ModuleAgregator
        self.m_BotMessages = a_BotMessages
        self.m_BotButtons = a_BotButtons
        self.m_Log = a_Log

        self.m_StartButtonName = self.CreateButton('start', a_StartButtonName)
        self.m_StartMessage = self.CreateMessage('start', a_StartMessage)

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
        return simple_message.WorkFuncResult(self.m_StartMessage)

    def CreateMessage(self, a_MessageName, a_MessageDesc):
        msg = self.m_BotMessages.CreateMessage(f'{self.GetName()} {a_MessageName}', a_MessageDesc, self.m_Log.GetTimeNow())
        return msg

    def CreateButton(self, a_ButtonName, a_ButtonDesc):
        btn = self.m_BotButtons.CreateMessage(f'{self.GetName()} {a_ButtonName}', a_ButtonDesc, self.m_Log.GetTimeNow())
        return btn

    def GetStartKeyboardButtons(self, a_Message, a_UserGroups):
        def GetButtons(a_ModNameList):
            buttons = []
            for n in a_ModNameList:
                m = self.m_ModuleAgregator.GetModule(n)
                b = m.GetModuleButtons()
                if not b is None or len(b) != 0:
                    buttons += b
            return buttons

        buttons = GetButtons(self.m_ChildModuleNameList)
        return keyboard.MakeButtons(buttons, a_UserGroups)

    def GetInitBDCommands(self):
        return [
                access.GetAccessForModuleRequest(self.GetName(), self.m_InitAccess, self.m_InitAccess),
                ]

    def GetAccess(self):
        return access.GetAccessForModule(self.m_Bot, self.GetName())

    def GetModuleButtons(self):
        return [
                keyboard.ButtonWithAccess(self.m_StartButtonName, user_access.AccessMode.VIEW, self.GetAccess()),
                ]

    def RegisterHandlers(self):
        self.m_Bot.RegisterMessageHandler(
                self.m_StartMessageHandler, 
                bd_item.GetCheckForTextFunc(self.m_StartButtonName)
                )

