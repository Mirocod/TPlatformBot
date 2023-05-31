# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Пользователи в группах

from bot_sys import bot_bd, keyboard, user_access, bd_table
from bot_modules import mod_table_operate, mod_simple_message
from bot_modules import access_utils, groups_utils
from template import bd_item, bd_item_add

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMAddUserInGroups(StatesGroup):
    bd_item = State()

from enum import Enum
from enum import auto

# ---------------------------------------------------------
# БД
module_name = 'user_in_groups'

table_name = groups_utils.table_user_in_groups_name
key_name = 'user_in_groupsID'
name_field = groups_utils.user_id_field
access_field = 'user_in_groupsAccess'
create_datetime_field = 'user_in_groupsCreateDateTime'
parent_id_field = groups_utils.parent_id_field

table_user_id_field = bd_table.TableField(name_field, bd_table.TableFieldDestiny.NAME, bd_table.TableFieldType.STR)
table_parent_id_field = bd_table.TableField(parent_id_field, bd_table.TableFieldDestiny.PARENT_ID, bd_table.TableFieldType.INT)

table = bd_table.Table(table_name, [
        bd_table.TableField(key_name, bd_table.TableFieldDestiny.KEY, bd_table.TableFieldType.INT),
        table_user_id_field,
        bd_table.TableField(access_field, bd_table.TableFieldDestiny.ACCESS, bd_table.TableFieldType.STR),
        bd_table.TableField(create_datetime_field, bd_table.TableFieldDestiny.CREATE_DATE, bd_table.TableFieldType.STR),
        table_parent_id_field,
        ],
        [
            [table_user_id_field, table_parent_id_field],
        ]
        )

init_access = f'{user_access.user_access_group_new}=-'

# ---------------------------------------------------------
# Сообщения и кнопки

class ButtonNames(Enum):
    ADD_USER = auto() 

button_names = {
    mod_simple_message.ButtonNames.START: "🗫 Пользователи в группах",
    mod_table_operate.ButtonNames.LIST: "📃 Список пользователей в группах",
    ButtonNames.ADD_USER: "✅ Добавить пользователя в группу",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.ACCESS): "✋ Доступ к пользователю в группе",
    mod_table_operate.ButtonNames.DEL: "❌ Удалить пользователя из группы",
}

messages = {
    mod_simple_message.Messages.START: f'''
<b>{button_names[mod_simple_message.ButtonNames.START]}</b>

''',
    mod_table_operate.Messages.SELECT: '''
Пожалуйста, выберите пользователя в группе:
''',
    mod_table_operate.Messages.ERROR_FIND: '''
❌ Ошибка, пользователь в группе не найден
''',
    mod_table_operate.Messages.OPEN: f'''
<b>пользователь в группе:  #{name_field}</b>

Группа: #{parent_id_field}

Время создания: #{create_datetime_field}
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.NAME): '''
Создание пользователя в группе.

Укажите ID пользователя:
''',
    mod_table_operate.Messages.SUCCESS_CREATE: '''✅ Пользователь успешно добавлен в группу!''',
    mod_table_operate.Messages.START_EDIT: '''
Пожалуйста, выберите действие:
''',
    mod_table_operate.Messages.SELECT_TO_EDIT: '''
Выберите пользователя в группе, которого вы хотите отредактировать.
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.ACCESS): f'''
Текущий доступ к пользователю в группе:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
''',
    mod_table_operate.Messages.SUCCESS_EDIT: '''✅ Пользователь в группе успешно отредактирован!''',
    mod_table_operate.Messages.SELECT_TO_DELETE: '''
Выберите пользователя в группе, которого вы хотите удалить.
''',
    mod_table_operate.Messages.SUCCESS_DELETE: '''✅ Пульзователь успешно удалён из группы!''',
}

class ModuleUserInGroups(mod_table_operate.TableOperateModule):
    def __init__(self, a_ParentModName, a_ChildModName, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(table, messages, button_names, a_ParentModName, a_ChildModName, init_access, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)

    def GetName(self):
        return module_name

    def GetStartKeyboardButtons(self, a_Message, a_UserGroups):
        t_buttons = super().GetStartKeyboardButtons(a_Message, a_UserGroups)
        cur_buttons = [
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.ADD_USER), user_access.AccessMode.ADD, self.GetAccess()),
                ]
        return t_buttons + keyboard.MakeButtons(self.m_Bot, cur_buttons, a_UserGroups)

    def RegisterHandlers(self):
        super().RegisterHandlers()
        GetButtonNameAndKeyValueAndAccess = self.m_GetButtonNameAndKeyValueAndAccessFunc
        GetAccess = self.m_GetAccessFunc

        defaul_keyboard_func = self.m_GetStartKeyboardButtonsFunc

        parent_table_name = None
        parent_key_name = None
        if self.m_ParentModName:
            parent_mod = self.GetModule(self.m_ParentModName)
            parent_table_name = parent_mod.m_Table.GetName()
            parent_key_name = parent_mod.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.KEY)

        # Добавление 
        a_ButtonName = self.GetButton(ButtonNames.ADD_USER)
        if a_ButtonName:
            a_Prefix = self.RegisterSelect(a_ButtonName, user_access.AccessMode.ADD, only_parent = True)

            check_func = bd_item.GetCheckForTextFunc(a_ButtonName)
            if a_Prefix:
                check_func = bd_item.GetCheckForPrefixFunc(a_Prefix)

            bd_item_add.AddBDItem1RegisterHandlers(self.m_Bot,\
                    check_func,\
                    FSMAddUserInGroups,\
                    self.m_AddBDItemFunc,\
                    self.ShowMessageTemplate(self.GetMessage(mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.NAME))),\
                    self.ShowMessageTemplate(self.GetMessage(mod_table_operate.Messages.SUCCESS_CREATE)),\
                    a_Prefix,\
                    parent_table_name,\
                    parent_key_name,\
                    name_field,\
                    GetButtonNameAndKeyValueAndAccess,\
                    GetAccess,\
                    defaul_keyboard_func,\
                    bd_item.FieldType.text,\
                    access_mode = user_access.AccessMode.ADD\
                    )


