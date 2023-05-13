#-*-coding utf-8-*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

from abc import ABC, abstractmethod

class IBot(ABC):
    @abstractmethod
    def GetRootIDs():
        pass

    @abstractmethod
    def GetLog():
        pass

    @abstractmethod
    def SQLRequest(self, a_Request : str, commit = False, return_error = False, param = None):
        pass

    @abstractmethod
    def GetUserGroupData(a_UserID):
        pass

    @abstractmethod
    def GetAccessForModule(a_ModuleName):
        pass

    @abstractmethod
    def GetItemDefaultAccessForModule(a_ModuleName):
        pass

    @abstractmethod
    async def SendMessage(self, a_UserID, a_Message, a_PhotoIDs, a_InlineKeyboardButtons, a_KeyboardButtons):
        pass

    @abstractmethod
    def RegisterMessageHandler(self, a_MessageHandler, a_CheckFunc):
        pass

    @abstractmethod
    def RegisterCallbackHandler(self, a_CallbackHandler, a_CheckFunc):
        pass

    @abstractmethod
    def StartPolling(self):
        pass

