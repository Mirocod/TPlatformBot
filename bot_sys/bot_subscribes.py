#-*-coding utf-8-*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Работа с подписками

from enum import Enum
from enum import auto

# Тип поля в таблице
class SubscribeType(Enum):
    ADD = auto()
    ANY_ITEM_DEL = auto()
    ANY_ITEM_EDIT = auto()
    ITEM_DEL = auto()
    ITEM_EDIT = auto()

class BotSubscribes
    def __init__(self):
        self.Clear()

    def GetSubscribes(self):
        return self.m_Subscribes

    def Clear(self):
        self.m_Subscribes = {}

    def CheckSubscribe(self, a_UserID, a_ModuleName, a_Type, a_ItemID = -1):
        s = self.GetSubscribes()
        su = s.get(a_UserID, None)
        if su:
            sub_um = su.get(a_ModuleName, None)
            if sub_um:
                t = su.get(a_ItemID, None)
                return t
        return None

    def AddSubscribe(self, a_UserID, a_ModuleName, a_Type, a_ItemID = -1):
        s = self.GetSubscribes()
        if not s.get(a_UserID, None):
            s[a_UserID] = {}
        if not s[a_UserID].get(a_ModuleName, None):
            s[a_UserID][a_ModuleName] = {}
        s[a_UserID][a_ModuleName][a_ItemID] = a_Type
