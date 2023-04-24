#-*-coding utf-8-*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Доступ пользователей

from enum import Enum
from bot_sys import config

user_access_readme = '''
Доступ к пользователям задаётся в виде строки
`user1=daver;user2=av;Group1=v;Group2=-;Group3=+;other=-`
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
группа 'other' - остальные
'''

# ---------------------------------------------------------
# Типы уровня доступа

class AccessMode(Enum):
    VIEW = 'v'
    ADD = 'a'
    EDIT = 'e'
    DELETE = 'd'
    ACCEES_EDIT = 'r'

class UserGroups:
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

# Возвращает возможность доступа пользователю a_UserGroups в элемент с правами a_AccessValue по режиму доступа a_AccessMode
def CheckAccessString(a_AccessValue : str, a_UserGroups : UserGroups, a_AccessMode : AccessMode):
    if a_UserGroups.user_id in config.GetRootIDs():
        return True
    for i in a_AccessValue.split(';'):
        d = i.split('=')
        if len(d) != 2:
            continue
        name = d[0]
        access = d[1]
        if name == a_UserGroups.user_id or name in a_UserGroups.group_names_list or name == 'other':
            if CheckAccessItem(access, a_AccessMode):
                return True
    return False

def Test():
    for am in AccessMode.ADD, AccessMode.DELETE, AccessMode.EDIT, AccessMode.VIEW, AccessMode.ACCEES_EDIT:
        assert CheckAccessString('1234=+', UserGroups('1234', []), am)
        assert not CheckAccessString('1234=-', UserGroups('1234', []), am)
        assert CheckAccessString('1234=+;gr1=+', UserGroups('1234', ['gr1']), am)
        assert CheckAccessString('1234=-;gr1=+', UserGroups('1234', ['gr1']), am)
        assert not CheckAccessString('1234=+', UserGroups('123', []), am)
        assert not CheckAccessString('1234=-', UserGroups('123', []), am)
        assert not CheckAccessString('1234=+;gr1=+', UserGroups('123', ['gr']), am)
        assert not CheckAccessString('1234=-;gr1=+', UserGroups('123', ['gr']), am)
        assert not CheckAccessString('1234=+;gr=+', UserGroups('123', ['gr1']), am)
        assert not CheckAccessString('1234=-;gr=+', UserGroups('123', ['gr1']), am)

    assert CheckAccessString('123=-;1234=a', UserGroups('1234', []), AccessMode.ADD)
    assert CheckAccessString('123=-;1234=d', UserGroups('1234', []), AccessMode.DELETE)
    assert CheckAccessString('123=-;1234=e', UserGroups('1234', []), AccessMode.EDIT)
    assert CheckAccessString('123=-;1234=r', UserGroups('1234', []), AccessMode.ACCEES_EDIT)
    assert CheckAccessString('123=-;1234=v', UserGroups('1234', []), AccessMode.VIEW)
    assert CheckAccessString('123=-;gr1=a', UserGroups('1234', ['gr1']), AccessMode.ADD)
    assert CheckAccessString('123=-;gr1=d', UserGroups('1234', ['gr1']), AccessMode.DELETE)
    assert CheckAccessString('123=-;gr1=e', UserGroups('1234', ['gr1']), AccessMode.EDIT)
    assert CheckAccessString('123=-;gr1=r', UserGroups('1234', ['gr1']), AccessMode.ACCEES_EDIT)
    assert CheckAccessString('123=-;gr1=v', UserGroups('1234', ['gr1']), AccessMode.VIEW)
    assert CheckAccessString('123=-;1234=daver', UserGroups('1234', []), AccessMode.ADD)
    assert CheckAccessString('123=-;1234=dav', UserGroups('1234', []), AccessMode.DELETE)
    assert CheckAccessString('123=-;1234=edv', UserGroups('1234', []), AccessMode.EDIT)
    assert CheckAccessString('123=-;1234=rav', UserGroups('1234', []), AccessMode.ACCEES_EDIT)
    assert CheckAccessString('123=-;1234=va', UserGroups('1234', []), AccessMode.VIEW)
    assert CheckAccessString('123=-;gr1=avr', UserGroups('1234', ['gr1']), AccessMode.ADD)
    assert CheckAccessString('123=-;gr1=daver', UserGroups('1234', ['gr1']), AccessMode.DELETE)
    assert CheckAccessString('123=-;gr1=eva', UserGroups('1234', ['gr1']), AccessMode.EDIT)
    assert CheckAccessString('123=-;gr1=re', UserGroups('1234', ['gr1']), AccessMode.ACCEES_EDIT)
    assert CheckAccessString('123=-;gr1=vad', UserGroups('1234', ['gr1']), AccessMode.VIEW)

    assert not CheckAccessString('123=-;1234=d', UserGroups('1234', []), AccessMode.ADD)
    assert not CheckAccessString('123=-;1234=a', UserGroups('1234', []), AccessMode.DELETE)
    assert not CheckAccessString('123=-;1234=r', UserGroups('1234', []), AccessMode.EDIT)
    assert not CheckAccessString('123=-;1234=v', UserGroups('1234', []), AccessMode.ACCEES_EDIT)
    assert not CheckAccessString('123=-;1234=e', UserGroups('1234', []), AccessMode.VIEW)
    assert not CheckAccessString('123=-;gr1=d', UserGroups('1234', ['gr']), AccessMode.ADD)
    assert not CheckAccessString('123=-;gr1=a', UserGroups('1234', ['gr']), AccessMode.DELETE)
    assert not CheckAccessString('123=-;gr1=v', UserGroups('1234', ['gr']), AccessMode.EDIT)
    assert not CheckAccessString('123=-;gr1=e', UserGroups('1234', ['gr']), AccessMode.ACCEES_EDIT)
    assert not CheckAccessString('123=-;gr1=r', UserGroups('1234', ['gr']), AccessMode.VIEW)
    assert not CheckAccessString('123=-;1234=dver', UserGroups('1234', []), AccessMode.ADD)
    assert not CheckAccessString('123=-;1234=av', UserGroups('1234', []), AccessMode.DELETE)
    assert not CheckAccessString('123=-;1234=dv', UserGroups('1234', []), AccessMode.EDIT)
    assert not CheckAccessString('123=-;1234=av', UserGroups('1234', []), AccessMode.ACCEES_EDIT)
    assert not CheckAccessString('123=-;1234=a', UserGroups('1234', []), AccessMode.VIEW)
    assert not CheckAccessString('123=-;gr1=vr', UserGroups('1234', ['gr']), AccessMode.ADD)
    assert not CheckAccessString('123=-;gr1=aver', UserGroups('1234', ['gr']), AccessMode.DELETE)
    assert not CheckAccessString('123=-;gr1=va', UserGroups('1234', ['gr']), AccessMode.EDIT)
    assert not CheckAccessString('123=-;gr1=ea', UserGroups('1234', ['gr']), AccessMode.ACCEES_EDIT)
    assert not CheckAccessString('123=-;gr1=ad', UserGroups('1234', ['gr']), AccessMode.VIEW)

    assert CheckAccessString('123=-;other=a', UserGroups('1234', []), AccessMode.ADD)
    assert CheckAccessString('123=-;other=d', UserGroups('1234', []), AccessMode.DELETE)
    assert CheckAccessString('123=-;other=e', UserGroups('1234', []), AccessMode.EDIT)
    assert CheckAccessString('123=-;other=r', UserGroups('1234', []), AccessMode.ACCEES_EDIT)
    assert CheckAccessString('123=-;other=v', UserGroups('1234', []), AccessMode.VIEW)
    assert CheckAccessString('123=-;other=a', UserGroups('1234', ['gr1']), AccessMode.ADD)
    assert CheckAccessString('123=-;other=d', UserGroups('1234', ['gr1']), AccessMode.DELETE)
    assert CheckAccessString('123=-;other=e', UserGroups('1234', ['gr1']), AccessMode.EDIT)
    assert CheckAccessString('123=-;other=r', UserGroups('1234', ['gr1']), AccessMode.ACCEES_EDIT)
    assert CheckAccessString('123=-;other=v', UserGroups('1234', ['gr1']), AccessMode.VIEW)
    assert CheckAccessString('123=-;other=daver', UserGroups('1234', []), AccessMode.ADD)
    assert CheckAccessString('123=-;other=dav', UserGroups('1234', []), AccessMode.DELETE)
    assert CheckAccessString('123=-;other=edv', UserGroups('1234', []), AccessMode.EDIT)
    assert CheckAccessString('123=-;other=rav', UserGroups('1234', []), AccessMode.ACCEES_EDIT)
    assert CheckAccessString('123=-;other=va', UserGroups('1234', []), AccessMode.VIEW)
    assert CheckAccessString('123=-;other=avr', UserGroups('1234', ['gr1']), AccessMode.ADD)
    assert CheckAccessString('123=-;other=daver', UserGroups('1234', ['gr1']), AccessMode.DELETE)
    assert CheckAccessString('123=-;other=eva', UserGroups('1234', ['gr1']), AccessMode.EDIT)
    assert CheckAccessString('123=-;other=re', UserGroups('1234', ['gr1']), AccessMode.ACCEES_EDIT)
    assert CheckAccessString('123=-;other=vad', UserGroups('1234', ['gr1']), AccessMode.VIEW)

    assert not CheckAccessString('123=-;other=d', UserGroups('1234', []), AccessMode.ADD)
    assert not CheckAccessString('123=-;other=a', UserGroups('1234', []), AccessMode.DELETE)
    assert not CheckAccessString('123=-;other=r', UserGroups('1234', []), AccessMode.EDIT)
    assert not CheckAccessString('123=-;other=v', UserGroups('1234', []), AccessMode.ACCEES_EDIT)
    assert not CheckAccessString('123=-;other=e', UserGroups('1234', []), AccessMode.VIEW)
    assert not CheckAccessString('123=-;gr1=d;other=-', UserGroups('1234', ['gr']), AccessMode.ADD)
    assert not CheckAccessString('123=-;gr1=a;other=-', UserGroups('1234', ['gr']), AccessMode.DELETE)
    assert not CheckAccessString('123=-;gr1=v;other=-', UserGroups('1234', ['gr']), AccessMode.EDIT)
    assert not CheckAccessString('123=-;gr1=e;other=-', UserGroups('1234', ['gr']), AccessMode.ACCEES_EDIT)
    assert not CheckAccessString('123=-;gr1=r;other=-', UserGroups('1234', ['gr']), AccessMode.VIEW)
    assert not CheckAccessString('123=-;other=dver', UserGroups('1234', []), AccessMode.ADD)
    assert not CheckAccessString('123=-;other=av', UserGroups('1234', []), AccessMode.DELETE)
    assert not CheckAccessString('123=-;other=dv', UserGroups('1234', []), AccessMode.EDIT)
    assert not CheckAccessString('123=-;other=av', UserGroups('1234', []), AccessMode.ACCEES_EDIT)
    assert not CheckAccessString('123=-;other=a', UserGroups('1234', []), AccessMode.VIEW)
    assert not CheckAccessString('123=-;other=vr', UserGroups('1234', ['gr']), AccessMode.ADD)
    assert not CheckAccessString('123=-;other=aver', UserGroups('1234', ['gr']), AccessMode.DELETE)
    assert not CheckAccessString('123=-;other=va', UserGroups('1234', ['gr']), AccessMode.EDIT)
    assert not CheckAccessString('123=-;other=ea', UserGroups('1234', ['gr']), AccessMode.ACCEES_EDIT)
    assert not CheckAccessString('123=-;other=ad', UserGroups('1234', ['gr']), AccessMode.VIEW)

