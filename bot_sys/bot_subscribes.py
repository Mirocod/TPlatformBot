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

class BotSubscribes:
    def __init__(self):
        self.Clear()

    def GetSubscribes(self):
        return self.m_Subscribes

    def Clear(self):
        self.m_Subscribes = {}

    def GetUserIDs(self, a_ModuleName, a_Type, a_ItemID = -1):
        s = self.GetSubscribes()
        ids = set()
        for user_id, su in s.items():
            sub_um = su.get(a_ModuleName, None)
            if sub_um:
                t = sub_um.get(a_ItemID, None)
                if t == a_Type:
                    ids.add(user_id)
        return ids

    def AddSubscribe(self, a_UserID, a_ModuleName, a_Type, a_ItemID = -1):
        s = self.GetSubscribes()
        if not s.get(a_UserID, None):
            s[a_UserID] = {}
        if not s[a_UserID].get(a_ModuleName, None):
            s[a_UserID][a_ModuleName] = {}
        s[a_UserID][a_ModuleName][a_ItemID] = a_Type

def Test():
    a = set()
    a.add(1)
    a.add(2)
    a.add(1)
    assert 1 in a
    assert not 3 in a

    user_id_1 = '123'
    user_id_2 = '34234'
    user_id_3 = '4234'
    mod_1 = 'proj'
    mod_2 = 'backup'
    s = BotSubscribes()
    s.AddSubscribe(user_id_1, mod_1, SubscribeType.ADD)
    s.AddSubscribe(user_id_2, mod_2, SubscribeType.ITEM_DEL)

    assert len(s.GetUserIDs(mod_1, SubscribeType.ADD)) == 1
    assert len(s.GetUserIDs(mod_1, SubscribeType.ANY_ITEM_DEL)) == 0
    assert user_id_1 in s.GetUserIDs(mod_1, SubscribeType.ADD)
    assert not user_id_2 in s.GetUserIDs(mod_1, SubscribeType.ADD)
    assert not user_id_3 in s.GetUserIDs(mod_1, SubscribeType.ADD)

    assert len(s.GetUserIDs(mod_2, SubscribeType.ITEM_DEL)) == 1
    assert len(s.GetUserIDs(mod_2, SubscribeType.ADD)) == 0
    assert user_id_2 in s.GetUserIDs(mod_2, SubscribeType.ITEM_DEL)
    assert not user_id_1 in s.GetUserIDs(mod_2, SubscribeType.ITEM_DEL)
    assert not user_id_3 in s.GetUserIDs(mod_2, SubscribeType.ITEM_DEL)
