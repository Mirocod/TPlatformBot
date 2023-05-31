# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Пользователи

from bot_sys import bot_bd, keyboard, user_access, bd_table
from bot_modules import mod_table_operate, mod_simple_message
from bot_modules import access_utils, groups_utils, groups, user_in_groups

# ---------------------------------------------------------
# БД
module_name = 'users'

table_name = module_name
key_name = 'user_id'
name_field = 'userName'
name1_field = 'userFirstName'
name2_field = 'userLastName'
is_bot_field = 'userIsBot'
language_code_field = 'userLanguageCode'
photo_field = 'userPhoto'
access_field = 'userAccess'
create_datetime_field = 'createDateTime'

table = bd_table.Table(table_name, [
        bd_table.TableField(key_name, bd_table.TableFieldDestiny.KEY, bd_table.TableFieldType.INT),
        bd_table.TableField(name_field, bd_table.TableFieldDestiny.NAME, bd_table.TableFieldType.STR),
        bd_table.TableField(name1_field, bd_table.TableFieldDestiny.DESC, bd_table.TableFieldType.STR),
        bd_table.TableField(name2_field, bd_table.TableFieldDestiny.DESC, bd_table.TableFieldType.STR),
        bd_table.TableField(is_bot_field, bd_table.TableFieldDestiny.DESC, bd_table.TableFieldType.STR),
        bd_table.TableField(language_code_field, bd_table.TableFieldDestiny.DESC, bd_table.TableFieldType.STR),
        bd_table.TableField(photo_field, bd_table.TableFieldDestiny.PHOTO, bd_table.TableFieldType.STR),
        bd_table.TableField(access_field, bd_table.TableFieldDestiny.ACCESS, bd_table.TableFieldType.STR),
        bd_table.TableField(create_datetime_field, bd_table.TableFieldDestiny.CREATE_DATE, bd_table.TableFieldType.STR),
        ])

init_access = f'{user_access.user_access_group_new}=v'

# ---------------------------------------------------------
# Сообщения и кнопки

button_names = {
    mod_simple_message.ButtonNames.START: "👤 Пользователи",
    mod_table_operate.ButtonNames.LIST: "📃 Список пользователей",
#    mod_table_operate.ButtonNames.ADD: "✅ Добавить пользователя",
    mod_table_operate.ButtonNames.EDIT: "🛠 Редактировать пользователя",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.PHOTO): "☐ Изменить изображение в пользователяе",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.NAME): "≂ Изменить название в пользователяе",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.DESC): "𝌴 Изменить описание в пользователяе",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.ACCESS): "✋ Изменить доступ к пользователю",
    mod_table_operate.ButtonNames.DEL: "❌ Удалить пользователя",
}

messages = {
    mod_simple_message.Messages.START: f'''
<b>{button_names[mod_simple_message.ButtonNames.START]}</b>

''',
    mod_table_operate.Messages.SELECT: '''
Пожалуйста, выберите пользователя:
''',
    mod_table_operate.Messages.ERROR_FIND: '''
❌ Ошибка, пользователя не найден
''',
    mod_table_operate.Messages.OPEN: f'''
<b>Пользователь:  #{name_field}</b>

<b>ID:</b> #{key_name}
<b>Имя:</b> #{name_field}
<b>Имя1:</b> #{name1_field}
<b>Имя2:</b> #{name2_field}
<b>Код языка:</b> #{language_code_field}
<b>Дата добавления:</b> #{create_datetime_field}
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.NAME): '''
Создание пользователя. Шаг №1

Введите название пользователя:
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.DESC): '''
Создание пользователя. Шаг №2

Введите описание пользователя:
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.PHOTO): '''
Создание пользователя. Шаг №3

Загрузите обложку для пользователя (Фото):
Она будет отображаться в его описании.
''',
    mod_table_operate.Messages.SUCCESS_CREATE: '''✅ Пользователь успешно добавлен!''',
    mod_table_operate.Messages.START_EDIT: '''
Пожалуйста, выберите действие:
''',
    mod_table_operate.Messages.SELECT_TO_EDIT: '''
Выберите пользователя, которого вы хотите отредактировать.
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.PHOTO): '''
Загрузите новую обложку для пользователя (Фото):
Она будет отображаться в его описании.
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.NAME): f'''
Текущее название пользователя:
#{name_field}

Введите новое название пользователя:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.DESC): f'''
Текущее описание пользователя:
#{name1_field}

Введите новое описание пользователя:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.ACCESS): f'''
Текущий доступ к пользователю:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
''',
    mod_table_operate.Messages.SUCCESS_EDIT: '''✅ Пользователь успешно отредактирован!''',
    mod_table_operate.Messages.SELECT_TO_DELETE: '''
Выберите пользователя, который вы хотите удалить.
''',
    mod_table_operate.Messages.SUCCESS_DELETE: '''✅ Пользователь успешно удалён!''',
}

class ModuleUsers(mod_table_operate.TableOperateModule):
    def __init__(self, a_ParentModName, a_ChildModName, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(table, messages, button_names, a_ParentModName, a_ChildModName, init_access, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)

    def GetName(self):
        return module_name


# Работа с базой данных пользователей

# Добавление пользователя, если он уже есть, то игнорируем
def AddUser(a_Bot, a_UserID, a_UserName, a_UserName1, a_UserName2, a_UserIsBot, a_LanguageCode):
    a_Bot.SQLRequest(f"INSERT OR IGNORE INTO users ({key_name}, {name_field}, {name1_field}, {name2_field}, {is_bot_field}, {language_code_field}, {photo_field}, {access_field}, {create_datetime_field}) VALUES (?, ?, ?, ?, ?, ?, 0, ?, {bot_bd.GetBDDateTimeNow()});", 
            commit=True, param = (a_UserID, a_UserName, a_UserName1, a_UserName2, a_UserIsBot, a_LanguageCode, access_utils.GetItemDefaultAccessForModule(a_Bot, module_name)))

    user_groups = groups_utils.GetUserGroupData(a_Bot, a_UserID)
    # Если пользователь не состоит ни в одной группе, то добавляем его в группу user_access.user_access_group_new
    if len(user_groups.group_names_list) == 0:
        new_group_id = a_Bot.SQLRequest(f'SELECT {groups.key_name} FROM {groups.table_name} WHERE {groups.name_field} = ?', 
                param = [user_access.user_access_group_new])
        if new_group_id and new_group_id[0]:
            a_Bot.SQLRequest(f"INSERT OR IGNORE INTO {user_in_groups.table_name} ({user_in_groups.name_field}, {user_in_groups.parent_id_field}, {user_in_groups.access_field}, {user_in_groups.create_datetime_field}) VALUES (?, ?, ?, {bot_bd.GetBDDateTimeNow()});", 
                    commit=True, param = (a_UserID, new_group_id[0][0], access_utils.GetItemDefaultAccessForModule(a_Bot, module_name)))

def GetUserInfo(a_Bot, a_UserID):
    user_info = a_Bot.SQLRequest('SELECT * FROM users WHERE user_id = ?', param = [a_UserID])
    if len(user_info) != 0:
        return user_info[0]
    return None
