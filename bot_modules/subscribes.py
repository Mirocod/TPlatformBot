# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Заказы

from bot_sys import bot_bd, keyboard, user_access, bd_table, bot_subscribes
from bot_modules import mod_table_operate, mod_simple_message
from template import bd_item_select, bd_item_view, bd_item

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMAddSubsType(StatesGroup):
    bd_item = State()

# ---------------------------------------------------------
# БД
module_name = 'subscribes'

table_name = module_name
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

init_access = f'{user_access.user_access_group_new}=vea'

class ButtonNames(Enum):
    ADD_SUBS = auto() 

button_names = {
    mod_simple_message.ButtonNames.START: "‍🛒 Подписки",
    mod_table_operate.ButtonNames.LIST: "📃 Список моих текущих подписок",
    mod_table_operate.ButtonNames.ADD_SUBS: "✅ Добавить подписку",
    mod_table_operate.ButtonNames.EDIT: "🛠 Редактировать мою подписку",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.NAME): "≂ Изменить название модуля в моей подписке",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.SUBSCRIBE_TYPE): "𝌴 Изменить тип в моей подписке",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.ITEM_ID): "𝌴 Изменить номер элемента в моей подписке",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.ACCESS): "✋ Изменить доступ к моей подписке",
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
<b>Подписку: #{name_field}</b>

<b>Описание и состав подписки:</b> #{desc_field}

<b>Статус:</b> #{status_field}

<b>Адрес доставки:</b> #{address_field}

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
    mod_table_operate.Messages.SUCCESS_CREATE: '''✅ Подписку успешно добавлен!''',
    mod_table_operate.Messages.START_EDIT: '''
Пожалуйста, выберите действие:
''',
    mod_table_operate.Messages.SELECT_TO_EDIT: '''
Выберите подписку, который вы хотите отредактировать.
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.NAME): f'''
Текущее название подписки:
#{name_field}

Введите новое название подписки:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.SUBSCRIBE_TYPE): f'''
Текущее описание подписки:
#{desc_field}

Введите новый тип подписки:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.ITEM_ID): f'''
Текущий адрес подписки:
#{desc_field}

Введите новый номер элемента:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.ACCESS): f'''
Текущий доступ к подпискуу:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
''',
    mod_table_operate.Messages.SUCCESS_EDIT: '''✅ Подписку успешно отредактировано!''',
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

        # Добавление 
        a_ButtonName = self.GetButton(ButtonNames.ADD_SUBS)
        if a_ButtonName:
            a_Prefix = self.RegisterSelect(a_ButtonName, user_access.AccessMode.ADD, only_parent = True)

            check_func = bd_item.GetCheckForTextFunc(a_ButtonName)
            if a_Prefix:
                check_func = bd_item.GetCheckForPrefixFunc(a_Prefix)

            bd_item_add.AddBDItem1RegisterHandlers(self.m_Bot,\
                    check_func,\
                    FSMAddSubsType,\
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

class ModuleUserSubscribe(ModuleOrders):
    def __init__(self, a_ParentModName, a_ChildModName, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(table, messages, button_names, a_ParentModName, a_ChildModName, init_access, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)

    def GetName(self):
        return module_name
