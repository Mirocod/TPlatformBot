#-*-coding utf-8-*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Доступ пользователей

from enum import Enum
from bot_sys import config

user_access_group_all = 'all'
user_access_group_new = 'new'

user_access_readme = f'''
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
группа '{user_access_group_new}' - новые участники (все новые участники автоматически добавляются в эту группу)
группа '{user_access_group_all}' - все
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
        self.user_id = str(a_UserID)
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
        if name == a_UserGroups.user_id or name in a_UserGroups.group_names_list or name == user_access_group_all:
            if CheckAccessItem(access, a_AccessMode):
                return True
    return False

def Test():
    assert '1234' in ['123', '1234']
    assert not '1234' in ['123', '12345']

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

    assert CheckAccessString(f'123=-;{user_access_group_all}=a', UserGroups('1234', []), AccessMode.ADD)
    assert CheckAccessString(f'123=-;{user_access_group_all}=d', UserGroups('1234', []), AccessMode.DELETE)
    assert CheckAccessString(f'123=-;{user_access_group_all}=e', UserGroups('1234', []), AccessMode.EDIT)
    assert CheckAccessString(f'123=-;{user_access_group_all}=r', UserGroups('1234', []), AccessMode.ACCEES_EDIT)
    assert CheckAccessString(f'123=-;{user_access_group_all}=v', UserGroups('1234', []), AccessMode.VIEW)
    assert CheckAccessString(f'123=-;{user_access_group_all}=a', UserGroups('1234', ['gr1']), AccessMode.ADD)
    assert CheckAccessString(f'123=-;{user_access_group_all}=d', UserGroups('1234', ['gr1']), AccessMode.DELETE)
    assert CheckAccessString(f'123=-;{user_access_group_all}=e', UserGroups('1234', ['gr1']), AccessMode.EDIT)
    assert CheckAccessString(f'123=-;{user_access_group_all}=r', UserGroups('1234', ['gr1']), AccessMode.ACCEES_EDIT)
    assert CheckAccessString(f'123=-;{user_access_group_all}=v', UserGroups('1234', ['gr1']), AccessMode.VIEW)
    assert CheckAccessString(f'123=-;{user_access_group_all}=daver', UserGroups('1234', []), AccessMode.ADD)
    assert CheckAccessString(f'123=-;{user_access_group_all}=dav', UserGroups('1234', []), AccessMode.DELETE)
    assert CheckAccessString(f'123=-;{user_access_group_all}=edv', UserGroups('1234', []), AccessMode.EDIT)
    assert CheckAccessString(f'123=-;{user_access_group_all}=rav', UserGroups('1234', []), AccessMode.ACCEES_EDIT)
    assert CheckAccessString(f'123=-;{user_access_group_all}=va', UserGroups('1234', []), AccessMode.VIEW)
    assert CheckAccessString(f'123=-;{user_access_group_all}=avr', UserGroups('1234', ['gr1']), AccessMode.ADD)
    assert CheckAccessString(f'123=-;{user_access_group_all}=daver', UserGroups('1234', ['gr1']), AccessMode.DELETE)
    assert CheckAccessString(f'123=-;{user_access_group_all}=eva', UserGroups('1234', ['gr1']), AccessMode.EDIT)
    assert CheckAccessString(f'123=-;{user_access_group_all}=re', UserGroups('1234', ['gr1']), AccessMode.ACCEES_EDIT)
    assert CheckAccessString(f'123=-;{user_access_group_all}=vad', UserGroups('1234', ['gr1']), AccessMode.VIEW)

    assert not CheckAccessString(f'123=-;{user_access_group_all}=d', UserGroups('1234', []), AccessMode.ADD)
    assert not CheckAccessString(f'123=-;{user_access_group_all}=a', UserGroups('1234', []), AccessMode.DELETE)
    assert not CheckAccessString(f'123=-;{user_access_group_all}=r', UserGroups('1234', []), AccessMode.EDIT)
    assert not CheckAccessString(f'123=-;{user_access_group_all}=v', UserGroups('1234', []), AccessMode.ACCEES_EDIT)
    assert not CheckAccessString(f'123=-;{user_access_group_all}=e', UserGroups('1234', []), AccessMode.VIEW)
    assert not CheckAccessString(f'123=-;gr1=d;{user_access_group_all}=-', UserGroups('1234', ['gr']), AccessMode.ADD)
    assert not CheckAccessString(f'123=-;gr1=a;{user_access_group_all}=-', UserGroups('1234', ['gr']), AccessMode.DELETE)
    assert not CheckAccessString(f'123=-;gr1=v;{user_access_group_all}=-', UserGroups('1234', ['gr']), AccessMode.EDIT)
    assert not CheckAccessString(f'123=-;gr1=e;{user_access_group_all}=-', UserGroups('1234', ['gr']), AccessMode.ACCEES_EDIT)
    assert not CheckAccessString(f'123=-;gr1=r;{user_access_group_all}=-', UserGroups('1234', ['gr']), AccessMode.VIEW)
    assert not CheckAccessString(f'123=-;{user_access_group_all}=dver', UserGroups('1234', []), AccessMode.ADD)
    assert not CheckAccessString(f'123=-;{user_access_group_all}=av', UserGroups('1234', []), AccessMode.DELETE)
    assert not CheckAccessString(f'123=-;{user_access_group_all}=dv', UserGroups('1234', []), AccessMode.EDIT)
    assert not CheckAccessString(f'123=-;{user_access_group_all}=av', UserGroups('1234', []), AccessMode.ACCEES_EDIT)
    assert not CheckAccessString(f'123=-;{user_access_group_all}=a', UserGroups('1234', []), AccessMode.VIEW)
    assert not CheckAccessString(f'123=-;{user_access_group_all}=vr', UserGroups('1234', ['gr']), AccessMode.ADD)
    assert not CheckAccessString(f'123=-;{user_access_group_all}=aver', UserGroups('1234', ['gr']), AccessMode.DELETE)
    assert not CheckAccessString(f'123=-;{user_access_group_all}=va', UserGroups('1234', ['gr']), AccessMode.EDIT)
    assert not CheckAccessString(f'123=-;{user_access_group_all}=ea', UserGroups('1234', ['gr']), AccessMode.ACCEES_EDIT)
    assert not CheckAccessString(f'123=-;{user_access_group_all}=ad', UserGroups('1234', ['gr']), AccessMode.VIEW)

