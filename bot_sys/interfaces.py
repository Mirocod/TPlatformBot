#-*-coding utf-8-*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

from abc import ABC, abstractmethod

class IBot(ABC):
    @abstractmethod
    def GetRootIDs(self):
        pass

    @abstractmethod
    def GetLog(self):
        pass

    @abstractmethod
    def SQLRequest(self, a_Request : str, commit = False, return_error = False, param = None):
        pass

    @abstractmethod
    async def SendMessage(self, a_UserID, a_Message, a_PhotoIDs, a_InlineKeyboardButtons, a_KeyboardButtons):
        pass

    @abstractmethod
    def RegisterMessageHandler(self, a_MessageHandler, a_CheckFunc, commands=None, regexp=None, content_types=None, state=None):
        pass

    @abstractmethod
    def RegisterCallbackHandler(self, a_CallbackHandler, a_CheckFunc, commands=None, regexp=None, content_types=None, state=None):
        pass

    @abstractmethod
    def StartPolling(self):
        pass

