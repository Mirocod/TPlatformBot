# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Подписки

from bot_sys import bot_bd, keyboard, user_access, bd_table, bot_subscribes
from bot_modules import mod_table_operate, mod_simple_message
from template import bd_item_select, bd_item_view, bd_item

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from enum import Enum
from enum import auto

class FSMAddSubsType(StatesGroup):
    bd_item = State()

# ---------------------------------------------------------
# БД
module_name = 'subscribes'

table_name = module_name
key_field = 'subsKey'
mod_name_field = 'modName'
type_field = 'subsType'
item_id_field = 'itemID'
access_field = 'subsAccess'
create_datetime_field = 'subsCreateDateTime'
parent_id_field = 'userID'

table_mod_name_field = bd_table.TableField(mod_name_field, bd_table.TableFieldDestiny.NAME, bd_table.TableFieldType.STR)
table_type_field = bd_table.TableField(type_field, bd_table.TableFieldDestiny.SUBSCRIBE_TYPE, bd_table.TableFieldType.ENUM, a_Enum = bot_subscribes.SubscribeType)
table_item_id_field = bd_table.TableField(item_id_field, bd_table.TableFieldDestiny.ITEM_ID, bd_table.TableFieldType.STR)
table_user_id_field = bd_table.TableField(parent_id_field, bd_table.TableFieldDestiny.PARENT_ID, bd_table.TableFieldType.STR)

table = bd_table.Table(table_name, [
        bd_table.TableField(key_field, bd_table.TableFieldDestiny.KEY, bd_table.TableFieldType.INT),
        table_mod_name_field,
        table_type_field,
        table_item_id_field,
        bd_table.TableField(access_field, bd_table.TableFieldDestiny.ACCESS, bd_table.TableFieldType.STR),
        bd_table.TableField(create_datetime_field, bd_table.TableFieldDestiny.CREATE_DATE, bd_table.TableFieldType.STR),
        table_user_id_field,
        ],
        [
            [table_mod_name_field, table_type_field, table_user_id_field, table_item_id_field],
        ]
        )

init_access = f'{user_access.user_access_group_new}=-'

button_names = {
    mod_simple_message.ButtonNames.START: "‍🛒 Подписки",
    mod_table_operate.ButtonNames.LIST: "📃 Список моих текущих подписок",
    mod_table_operate.ButtonNames.ADD: "✅ Добавить подписку",
    mod_table_operate.ButtonNames.EDIT: "🛠 Редактировать мою подписку",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.NAME): "≂ Изменить модуль в моей подписке",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.SUBSCRIBE_TYPE): "𝌴 Изменить тип в моей подписке",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.ITEM_ID): "𝌴 Изменить элемент в моей подписке",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.ACCESS): "✋ Изменить доступ к моей подписке",
    mod_table_operate.EnumButton(bot_subscribes.SubscribeType.ADD): "Добавление элемента",
    mod_table_operate.EnumButton(bot_subscribes.SubscribeType.ANY_ITEM_DEL): "Удаление какого либо элемента",
    mod_table_operate.EnumButton(bot_subscribes.SubscribeType.ANY_ITEM_EDIT): "Редактирование какого либо элемента",
    mod_table_operate.EnumButton(bot_subscribes.SubscribeType.ITEM_DEL): "Удаление определённого элемента",
    mod_table_operate.EnumButton(bot_subscribes.SubscribeType.ITEM_EDIT): "Редактирование определённого элемента",
    mod_table_operate.ButtonNames.DEL: "❌ Удалить мою подписку",
}

messages = {
    mod_simple_message.Messages.START: f'''
<b>{button_names[mod_simple_message.ButtonNames.START]}</b>

''',
    mod_table_operate.Messages.SELECT: '''
Пожалуйста, выберите подписку:
''',
    mod_table_operate.Messages.ERROR_FIND: '''
❌ Ошибка, подписку не найден
''',
    mod_table_operate.Messages.OPEN: f'''
<b>Подписку:</b>

<b>Название модуля:</b> #{mod_name_field}

<b>Тип:</b> #{type_field}

<b>Номер элемента:</b> #{item_id_field}

<b>Время создания:</b> #{create_datetime_field}
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.NAME): '''
Создание подписки. Шаг №1

Введите название модуля:
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.SUBSCRIBE_TYPE): '''
Создание подписки. Шаг №2

Введите тип подписки:
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.ITEM_ID): '''
Создание подписки. Шаг №3

Номер элемента, на который нужно подписаться (-1, если элемента нет):
''',
    mod_table_operate.Messages.SUCCESS_CREATE: '''✅ Подписка успешно добавлена!''',
    mod_table_operate.Messages.START_EDIT: '''
Пожалуйста, выберите действие:
''',
    mod_table_operate.Messages.SELECT_TO_EDIT: '''
Выберите подписку, который вы хотите отредактировать.
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.NAME): f'''
Текущее название модуля:
#{mod_name_field}

Введите новое название модуля:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.SUBSCRIBE_TYPE): f'''
Текущий тип подписки:
#{type_field}

Введите новый тип подписки:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.ITEM_ID): f'''
Текущий номер элемента: #{item_id_field}

Введите новый номер элемента:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.ACCESS): f'''
Текущий доступ к подписке:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
''',
    mod_table_operate.Messages.SUCCESS_EDIT: '''✅ Подписка успешно отредактирована!''',
    mod_table_operate.Messages.SELECT_TO_DELETE: '''
Выберите подписку, которую вы хотите удалить.
''',
    mod_table_operate.Messages.SUCCESS_DELETE: '''✅ Подписка успешно удалёна!''',
}

messages_subs_type_status = {
    mod_table_operate.EnumMessageForView(bot_subscribes.SubscribeType.ADD): f'''Добавление элемента''',
    mod_table_operate.EnumMessageForView(bot_subscribes.SubscribeType.ANY_ITEM_DEL): f'''Удаление элемента''',
    mod_table_operate.EnumMessageForView(bot_subscribes.SubscribeType.ANY_ITEM_EDIT): f'''Редактирование элемента''',
    mod_table_operate.EnumMessageForView(bot_subscribes.SubscribeType.ITEM_DEL): f'''Удаление конкретного элемента''',
    mod_table_operate.EnumMessageForView(bot_subscribes.SubscribeType.ITEM_EDIT): f'''Редактирование конкретного элемента''',
}

messages.update(messages_subs_type_status)

def GetCurItemsTemplate(a_Bot, a_TableName, a_UserIDFieldName, a_StatusFieldName):
    def GetBDItems(a_Message, a_UserGroups, a_ParentID):
        user_id = str(a_Message.from_user.id)
        request = f'SELECT * FROM {a_TableName} WHERE {a_UserIDFieldName} = ? AND {a_StatusFieldName} != ?'
        return a_Bot.SQLRequest(request, param = ([user_id, str(OrderStatus.FINISH)]))
    return GetBDItems

def GetBDItemsForUserTemplate(a_Bot, a_TableName, a_UserIDFieldName):
    def GetBDItems(a_Message, a_UserGroups, a_ParentID):
        user_id = str(a_Message.from_user.id)
        return bd_item.GetBDItemsTemplate(a_Bot, a_TableName, a_UserIDFieldName)(user_id)
    return GetBDItems

class DBItemForUserSelectSource(bd_item_select.DBItemSelectSource):
    def __init__(self, a_Bot, a_TableName, a_ParentIDFieldName, a_PrevPrefix, a_ButtonName):
        super().__init__(a_Bot, a_TableName, a_ParentIDFieldName, a_PrevPrefix, a_ButtonName)

    def GetItemsFunc(self):
        return GetBDItemsForUserTemplate(self.m_Bot, self.m_TableName, self.m_ParentIDFieldName)

    def IsFirst(self):
        return True

class ModuleSubscribe(mod_table_operate.TableOperateModule):
    def __init__(self, a_Table, a_Messages, a_Buttons, a_ParentModName, a_ChildModName, a_InitAccess, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(table, a_Messages, a_Buttons, a_ParentModName, a_ChildModName, a_InitAccess, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)

    def SelectSourceTemplate(self, a_PrevPrefix, a_ButtonName):
        parent_id_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PARENT_ID)
        return DBItemForUserSelectSource(self.m_Bot, self.m_Table.GetName(), parent_id_field, a_PrevPrefix, a_ButtonName)

    def AddBDItemFunc(self, a_ItemData, a_UserID):
        parent_id_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PARENT_ID)
        a_ItemData[parent_id_field] = a_UserID
        return super().AddBDItemFunc(a_ItemData, a_UserID)

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

    def GetButtonNameAndKeyValueAndAccess(self, a_Item):
        type_field_id = self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.SUBSCRIBE_TYPE)
        item_id_field_id = self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.ITEM_ID)
        n, k, a = super().GetButtonNameAndKeyValueAndAccess(a_Item)
        return n + ":" + str(a_Item[type_field_id]) + ":" + str(a_Item[item_id_field_id]), k, a

class ModuleUserSubscribe(ModuleSubscribe):
    def __init__(self, a_ParentModName, a_ChildModName, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(table, messages, button_names, a_ParentModName, a_ChildModName, init_access, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)

    def GetName(self):
        return module_name
