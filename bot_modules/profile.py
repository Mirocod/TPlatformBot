# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Профиль пользователя

from bot_sys import user_access, bot_bd, bd_table
from bot_modules import mod_simple_message, groups, access, access_utils, groups_utils
from template import bd_item, simple_message

# ---------------------------------------------------------
# БД
module_name = 'profile'

table_name = 'users'
key_name = 'user_id'
name_field = 'userName'
name1_field = 'userFirstName'
name2_field = 'userLastName'
is_bot_field = 'userIsBot'
language_code_field = 'userLanguageCode'
access_field = 'userAccess'
create_datetime_field = 'createDateTime'

table = bd_table.Table(table_name, [
        bd_table.TableField(key_name, bd_table.TableFieldDestiny.KEY, bd_table.TableFieldType.INT),
        bd_table.TableField(name_field, bd_table.TableFieldDestiny.NAME, bd_table.TableFieldType.STR),
        bd_table.TableField(name1_field, bd_table.TableFieldDestiny.DESC, bd_table.TableFieldType.STR),
        bd_table.TableField(name2_field, bd_table.TableFieldDestiny.DESC, bd_table.TableFieldType.STR),
        bd_table.TableField(is_bot_field, bd_table.TableFieldDestiny.DESC, bd_table.TableFieldType.STR),
        bd_table.TableField(language_code_field, bd_table.TableFieldDestiny.DESC, bd_table.TableFieldType.STR),
        bd_table.TableField(access_field, bd_table.TableFieldDestiny.ACCESS, bd_table.TableFieldType.STR),
        bd_table.TableField(create_datetime_field, bd_table.TableFieldDestiny.CREATE_DATE, bd_table.TableFieldType.STR),
        ])

start_message = f'''
<b>📰 Профиль:</b> 

<b>ID:</b> #{key_name}
<b>Имя:</b> #{name_field}
<b>Имя1:</b> #{name1_field}
<b>Имя2:</b> #{name2_field}
<b>Код языка:</b> #{language_code_field}
<b>Дата добавления:</b> #{create_datetime_field}
'''

start_button_name = "📰 Профиль"

init_access = f'{user_access.user_access_group_new}=+'

class ModuleProfile(mod_simple_message.SimpleMessageModule):
    def __init__(self, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(start_message, start_button_name, init_access, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)

    def GetInitBDCommands(self):
        return super(). GetInitBDCommands() + [
            table.GetInitTableRequest(),
            ]

    def GetName(self):
        return module_name

    # Основной обработчик главного сообщения
    async def StartMessageHandler(self, a_Message, state = None):
        user_info = GetUserInfo(self.m_Bot, a_Message.from_user.id)
        lang = str(a_Message.from_user.language_code)
        if not user_info is None:
            msg = self.m_StartMessage
            msg = msg.GetMessageForLang(lang).StaticCopy()
            msg.m_MessageDesc = table.ReplaceAllFieldTags(msg.GetDesc(), user_info)
            return simple_message.WorkFuncResult(msg, item_access = str(user_info[table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.ACCESS)]))
        return await super().StartMessageHandler(a_Message, state)


# Работа с базой данных пользователей

# Добавление пользователя, если он уже есть, то игнорируем
def AddUser(a_Bot, a_UserID, a_UserName, a_UserName1, a_UserName2, a_UserIsBot, a_LanguageCode):
    a_Bot.SQLRequest(f"INSERT OR IGNORE INTO users ({key_name}, {name_field}, {name1_field}, {name2_field}, {is_bot_field}, {language_code_field}, {access_field}, {create_datetime_field}) VALUES (?, ?, ?, ?, ?, ?, ?, {bot_bd.GetBDDateTimeNow()});", 
            commit=True, param = (a_UserID, a_UserName, a_UserName1, a_UserName2, a_UserIsBot, a_LanguageCode, access_utils.GetItemDefaultAccessForModule(a_Bot, module_name)))

    user_groups = groups_utils.GetUserGroupData(a_Bot, a_UserID)
    # Если пользователь не состоит ни в одной группе, то добавляем его в группу user_access.user_access_group_new
    if len(user_groups.group_names_list) == 0:
        new_group_id = a_Bot.SQLRequest(f'SELECT {groups.key_table_groups_name} FROM {groups.table_groups_name} WHERE {groups.name_table_groups_field} = ?', 
                param = [user_access.user_access_group_new])
        if new_group_id and new_group_id[0]:
            a_Bot.SQLRequest(f"INSERT OR IGNORE INTO {groups.table_user_in_groups_name} ({groups.user_id_field}, {groups.key_table_groups_name}, {groups.access_field}, {groups.create_datetime_field}) VALUES (?, ?, ?, {bot_bd.GetBDDateTimeNow()});", 
                    commit=True, param = (a_UserID, new_group_id[0][0], access_utils.GetItemDefaultAccessForModule(a_Bot, module_name)))

def GetUserInfo(a_Bot, a_UserID):
    user_info = a_Bot.SQLRequest('SELECT * FROM users WHERE user_id = ?', param = [a_UserID])
    if len(user_info) != 0:
        return user_info[0]
    return None
