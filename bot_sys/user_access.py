#-*-coding utf-8-*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Доступ пользователей

from enum import Enum
from bot_sys import config

user_access_readme = '''
Доступ к пользователям задаётся в виде строки
```
user1=daver;user2=av;Group1=v;Group2=-;Group3=+
```
Где через ';' располагаются различные варианты доступа
user1 и user2 - id пользоватлей
Group1, Group2, Group3 - Имена групп пользоватлей

Типы доступа:
VIEW = 'v' - чтение
ADD = 'a' - добавление
EDIT = 'e' - редактирование
DELETE = 'd' - удаление
ACCEES_EDIT = 'r' - изменение прав доступа
'+' - всё включено
'-' - всё выключено
'''

# ---------------------------------------------------------
# Типы уровня доступа

class AccessMode(Enum):
    VIEW = 'v'
    ADD = 'a'
    EDIT = 'e'
    DELETE = 'd'
    ACCEES_EDIT = 'r'

class UserAccess:
    def __init__(self, a_UserID : str, a_GroupNamesList : [str]):
        self.user_id = a_UserID
        self.group_names_list = a_GroupNamesList

# ---------------------------------------------------------
# Функции работы с уровнем доступа пользователей

def CheckAccessItem(a_AccessItem : str, a_AccessMode : AccessMode):
    if a_AccessItem == '+' or a_AccessMode.value in a_AccessItem:
        return True
    elif a_AccessItem == '-':
        return False
    return False

# Возвращает возможность доступа пользователю a_UserAccessData в элемент с правами a_AccessValue по режиму доступа a_AccessMode
def CheckAccessString(a_AccessValue : str, a_UserAccessData : UserAccess, a_AccessMode : AccessMode):
    if a_UserAccessData.user_id in config.GetRootIDs():
        return True
    for i in a_AccessValue.split(';'):
        d = i.split('=')
        if len(d) != 2:
            continue
        name = d[0]
        access = d[1]
        if name == a_UserAccessData.user_id or name in a_UserAccessData.group_names_list:
            if CheckAccessItem(access, a_AccessMode):
                return True
    return False

def Test():
    for am in AccessMode.ADD, AccessMode.DELETE, AccessMode.EDIT, AccessMode.VIEW, AccessMode.ACCEES_EDIT:
        assert CheckAccessString('1234=+', UserAccess('1234', []), am)
        assert not CheckAccessString('1234=-', UserAccess('1234', []), am)
        assert CheckAccessString('1234=+;gr1=+', UserAccess('1234', ['gr1']), am)
        assert CheckAccessString('1234=-;gr1=+', UserAccess('1234', ['gr1']), am)
        assert not CheckAccessString('1234=+', UserAccess('123', []), am)
        assert not CheckAccessString('1234=-', UserAccess('123', []), am)
        assert not CheckAccessString('1234=+;gr1=+', UserAccess('123', ['gr']), am)
        assert not CheckAccessString('1234=-;gr1=+', UserAccess('123', ['gr']), am)
        assert not CheckAccessString('1234=+;gr=+', UserAccess('123', ['gr1']), am)
        assert not CheckAccessString('1234=-;gr=+', UserAccess('123', ['gr1']), am)

    assert CheckAccessString('123=-;1234=a', UserAccess('1234', []), AccessMode.ADD)
    assert CheckAccessString('123=-;1234=d', UserAccess('1234', []), AccessMode.DELETE)
    assert CheckAccessString('123=-;1234=e', UserAccess('1234', []), AccessMode.EDIT)
    assert CheckAccessString('123=-;1234=r', UserAccess('1234', []), AccessMode.ACCEES_EDIT)
    assert CheckAccessString('123=-;1234=v', UserAccess('1234', []), AccessMode.VIEW)
    assert CheckAccessString('123=-;gr1=a', UserAccess('1234', ['gr1']), AccessMode.ADD)
    assert CheckAccessString('123=-;gr1=d', UserAccess('1234', ['gr1']), AccessMode.DELETE)
    assert CheckAccessString('123=-;gr1=e', UserAccess('1234', ['gr1']), AccessMode.EDIT)
    assert CheckAccessString('123=-;gr1=r', UserAccess('1234', ['gr1']), AccessMode.ACCEES_EDIT)
    assert CheckAccessString('123=-;gr1=v', UserAccess('1234', ['gr1']), AccessMode.VIEW)
    assert CheckAccessString('123=-;1234=daver', UserAccess('1234', []), AccessMode.ADD)
    assert CheckAccessString('123=-;1234=dav', UserAccess('1234', []), AccessMode.DELETE)
    assert CheckAccessString('123=-;1234=edv', UserAccess('1234', []), AccessMode.EDIT)
    assert CheckAccessString('123=-;1234=rav', UserAccess('1234', []), AccessMode.ACCEES_EDIT)
    assert CheckAccessString('123=-;1234=va', UserAccess('1234', []), AccessMode.VIEW)
    assert CheckAccessString('123=-;gr1=avr', UserAccess('1234', ['gr1']), AccessMode.ADD)
    assert CheckAccessString('123=-;gr1=daver', UserAccess('1234', ['gr1']), AccessMode.DELETE)
    assert CheckAccessString('123=-;gr1=eva', UserAccess('1234', ['gr1']), AccessMode.EDIT)
    assert CheckAccessString('123=-;gr1=re', UserAccess('1234', ['gr1']), AccessMode.ACCEES_EDIT)
    assert CheckAccessString('123=-;gr1=vad', UserAccess('1234', ['gr1']), AccessMode.VIEW)

    assert not CheckAccessString('123=-;1234=d', UserAccess('1234', []), AccessMode.ADD)
    assert not CheckAccessString('123=-;1234=a', UserAccess('1234', []), AccessMode.DELETE)
    assert not CheckAccessString('123=-;1234=r', UserAccess('1234', []), AccessMode.EDIT)
    assert not CheckAccessString('123=-;1234=v', UserAccess('1234', []), AccessMode.ACCEES_EDIT)
    assert not CheckAccessString('123=-;1234=e', UserAccess('1234', []), AccessMode.VIEW)
    assert not CheckAccessString('123=-;gr1=d', UserAccess('1234', ['gr']), AccessMode.ADD)
    assert not CheckAccessString('123=-;gr1=a', UserAccess('1234', ['gr']), AccessMode.DELETE)
    assert not CheckAccessString('123=-;gr1=v', UserAccess('1234', ['gr']), AccessMode.EDIT)
    assert not CheckAccessString('123=-;gr1=e', UserAccess('1234', ['gr']), AccessMode.ACCEES_EDIT)
    assert not CheckAccessString('123=-;gr1=r', UserAccess('1234', ['gr']), AccessMode.VIEW)
    assert not CheckAccessString('123=-;1234=dver', UserAccess('1234', []), AccessMode.ADD)
    assert not CheckAccessString('123=-;1234=av', UserAccess('1234', []), AccessMode.DELETE)
    assert not CheckAccessString('123=-;1234=dv', UserAccess('1234', []), AccessMode.EDIT)
    assert not CheckAccessString('123=-;1234=av', UserAccess('1234', []), AccessMode.ACCEES_EDIT)
    assert not CheckAccessString('123=-;1234=a', UserAccess('1234', []), AccessMode.VIEW)
    assert not CheckAccessString('123=-;gr1=vr', UserAccess('1234', ['gr']), AccessMode.ADD)
    assert not CheckAccessString('123=-;gr1=aver', UserAccess('1234', ['gr']), AccessMode.DELETE)
    assert not CheckAccessString('123=-;gr1=va', UserAccess('1234', ['gr']), AccessMode.EDIT)
    assert not CheckAccessString('123=-;gr1=ea', UserAccess('1234', ['gr']), AccessMode.ACCEES_EDIT)
    assert not CheckAccessString('123=-;gr1=ad', UserAccess('1234', ['gr']), AccessMode.VIEW)

