# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Заказы

from bot_sys import bot_bd, keyboard, user_access, bd_table
from bot_modules import mod_table_operate, mod_simple_message
from template import bd_item_select, bd_item_view, bd_item

from enum import Enum
from enum import auto

class OrderStatus(Enum):
    NEW = auto()
    PAY = auto()
    ADDRESS = auto()
    FINISH = auto()

# ---------------------------------------------------------
# БД
module_name = 'orders'

table_name = module_name
key_name = 'orderID'
name_field = 'orderName'
desc_field = 'orderDesc'
photo_field = 'orderPhoto'
status_field = 'orderStatus'
address_field = 'orderAddress'
access_field = 'orderAccess'
create_datetime_field = 'orderCreateDateTime'
parent_id_field = 'userID'

table = bd_table.Table(table_name, [
        bd_table.TableField(key_name, bd_table.TableFieldDestiny.KEY, bd_table.TableFieldType.INT),
        bd_table.TableField(name_field, bd_table.TableFieldDestiny.NAME, bd_table.TableFieldType.STR),
        bd_table.TableField(desc_field, bd_table.TableFieldDestiny.DESC, bd_table.TableFieldType.STR),
        bd_table.TableField(photo_field, bd_table.TableFieldDestiny.PHOTO, bd_table.TableFieldType.STR),
        bd_table.TableField(status_field, bd_table.TableFieldDestiny.STATUS, bd_table.TableFieldType.ENUM, a_Enum = OrderStatus),
        bd_table.TableField(address_field, bd_table.TableFieldDestiny.ADDRESS, bd_table.TableFieldType.STR),
        bd_table.TableField(access_field, bd_table.TableFieldDestiny.ACCESS, bd_table.TableFieldType.STR),
        bd_table.TableField(create_datetime_field, bd_table.TableFieldDestiny.CREATE_DATE, bd_table.TableFieldType.STR),
        bd_table.TableField(parent_id_field, bd_table.TableFieldDestiny.PARENT_ID, bd_table.TableFieldType.INT),
        ])

init_access = f'{user_access.user_access_group_new}=va'

# ---------------------------------------------------------
# Сообщения и кнопки

class ButtonNames(Enum):
    LIST_CURRENT = auto() 

button_names = {
    mod_simple_message.ButtonNames.START: "‍🛒 Заказы",
    mod_table_operate.ButtonNames.LIST: "📃 Список всех моих заказов",
    ButtonNames.LIST_CURRENT: "📃 Список моих текущих заказов",
    mod_table_operate.ButtonNames.ADD: "✅ Добавить заказ",
    mod_table_operate.ButtonNames.EDIT: "🛠 Редактировать мой заказ",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.PHOTO): "☐ Изменить изображение в моём заказе",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.NAME): "≂ Изменить название в моём заказе",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.DESC): "𝌴 Изменить описание в моём заказе",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.ADDRESS): "𝌴 Изменить адрес в моём заказе",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.ACCESS): "✋ Изменить доступ к моему заказу",
    mod_table_operate.ButtonNames.DEL: "❌ Удалить мой заказ",
}

messages = {
    mod_simple_message.Messages.START: f'''
<b>{button_names[mod_simple_message.ButtonNames.START]}</b>

''',
    mod_table_operate.Messages.SELECT: '''
Пожалуйста, выберите заказ:
''',
    mod_table_operate.Messages.ERROR_FIND: '''
❌ Ошибка, заказ не найден
''',
    mod_table_operate.Messages.OPEN: f'''
<b>Заказ: #{name_field}</b>

<b>Описание и состав заказа:</b> #{desc_field}

<b>Статус:</b> #{status_field}

<b>Адрес доставки:</b> #{address_field}

<b>Время создания:</b> #{create_datetime_field}
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.NAME): '''
Создание заказа. Шаг №1

Введите название заказа:
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.DESC): '''
Создание заказа. Шаг №2

Введите описание заказа:
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.PHOTO): '''
Создание заказа. Шаг №3

Загрузите обложку для заказа (Фото):
Она будет отображаться в его описании.
''',
    mod_table_operate.Messages.SUCCESS_CREATE: '''✅ Заказ успешно добавлен!''',
    mod_table_operate.Messages.START_EDIT: '''
Пожалуйста, выберите действие:
''',
    mod_table_operate.Messages.SELECT_TO_EDIT: '''
Выберите заказ, который вы хотите отредактировать.
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.PHOTO): '''
Загрузите новую обложку для заказа (Фото):
Она будет отображаться в его описании.
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.NAME): f'''
Текущее название заказа:
#{name_field}

Введите новое название заказа:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.DESC): f'''
Текущее описание заказа:
#{desc_field}

Введите новое описание заказа:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.ADDRESS): f'''
Текущий адрес заказа:
#{desc_field}

Введите новый адрес доставки заказа (укажите, кто, когда и где его сможет забрать):
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.ACCESS): f'''
Текущий доступ к заказу:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
''',
    mod_table_operate.Messages.SUCCESS_EDIT: '''✅ Заказ успешно отредактирован!''',
    mod_table_operate.Messages.SELECT_TO_DELETE: '''
Выберите заказ, который вы хотите удалить.
Все задачи и потребности в этом заказе так же будут удалены!
''',
    mod_table_operate.Messages.SUCCESS_DELETE: '''✅ Заказ успешно удалён!''',
}

messages_order_status = {
    mod_table_operate.EnumMessageForView(OrderStatus.NEW): f'''Заказ создан, ожидает модерации''',
    mod_table_operate.EnumMessageForView(OrderStatus.PAY): f'''Заказ ожидает оплаты''',
    mod_table_operate.EnumMessageForView(OrderStatus.ADDRESS): f'''Заказ ожидает указания адреса доставки''',
    mod_table_operate.EnumMessageForView(OrderStatus.FINISH): f'''Заказ выполнен''',
}

messages.update(messages_order_status)

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
    def __init__(self, a_Bot, a_TableName, a_ParentIDFieldName, a_PrevPrefix, a_ButtonName, a_OnlyCurrent = False):
        super().__init__(a_Bot, a_TableName, a_ParentIDFieldName, a_PrevPrefix, a_ButtonName)
        self.m_OnlyCurrent = a_OnlyCurrent

    def GetItemsFunc(self):
        if self.m_OnlyCurrent:
            return GetCurItemsTemplate(self.m_Bot, self.m_TableName, self.m_ParentIDFieldName, status_field)
        return GetBDItemsForUserTemplate(self.m_Bot, self.m_TableName, self.m_ParentIDFieldName)

    def IsFirst(self):
        return True

class ModuleOrders(mod_table_operate.TableOperateModule):
    def __init__(self, a_Table, a_Messages, a_Buttons, a_ParentModName, a_ChildModName, a_InitAccess, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(table, a_Messages, a_Buttons, a_ParentModName, a_ChildModName, a_InitAccess, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)

    def SelectSourceTemplate(self, a_PrevPrefix, a_ButtonName):
        parent_id_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PARENT_ID)
        return DBItemForUserSelectSource(self.m_Bot, self.m_Table.GetName(), parent_id_field, a_PrevPrefix, a_ButtonName)

    def SelectSourceForCurrentTemplate(self, a_PrevPrefix, a_ButtonName):
        parent_id_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PARENT_ID)
        return DBItemForUserSelectSource(self.m_Bot, self.m_Table.GetName(), parent_id_field, a_PrevPrefix, a_ButtonName, a_OnlyCurrent = True)

    def AddBDItemFunc(self, a_ItemData, a_UserID):
        parent_id_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PARENT_ID)
        a_ItemData[parent_id_field] = a_UserID
        a_ItemData[status_field] = str(OrderStatus.NEW)
        a_ItemData[address_field] = ''
        return super().AddBDItemFunc(a_ItemData, a_UserID)

    def GetStartKeyboardButtons(self, a_Message, a_UserGroups):
        parent_buttons = super().GetStartKeyboardButtons(a_Message, a_UserGroups)
        cur_buttons = [
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.LIST_CURRENT), user_access.AccessMode.VIEW, self.GetAccess()),
                ]
        return parent_buttons + keyboard.MakeButtons(self.m_Bot, cur_buttons, a_UserGroups)

    def RegisterHandlers(self):
        super().RegisterHandlers()
        table_name = self.m_Table.GetName()
        key_name = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.KEY)

        def GetViewItemInlineKeyboardTemplate(a_ItemID):
            return self.GetViewItemInlineKeyboardTemplate(a_ItemID)

        GetButtonNameAndKeyValueAndAccess = self.m_GetButtonNameAndKeyValueAndAccessFunc
        GetAccess = self.m_GetAccessFunc

        default_keyboard_func = self.m_GetStartKeyboardButtonsFunc

        # Список текущих, открытых заказов
        a_ButtonName = self.GetButton(ButtonNames.LIST_CURRENT)
        if a_ButtonName:
            a_Prefix = self.RegisterSelect(a_ButtonName, user_access.AccessMode.VIEW, only_parent = True)
            a_Prefix = bd_item_select.SelectRegisterHandlers(self.m_Bot,\
                    self.SelectSourceForCurrentTemplate(a_Prefix, a_ButtonName), \
                    GetButtonNameAndKeyValueAndAccess,\
                    self.GetMessage(mod_table_operate.Messages.SELECT),\
                    GetAccess,\
                    access_mode = user_access.AccessMode.VIEW\
                    )
            bd_item_view.ShowBDItemRegisterHandlers(self.m_Bot,\
                    a_Prefix,\
                    table_name,\
                    key_name,\
                    self.ShowMessageTemplate(self.GetMessage(mod_table_operate.Messages.OPEN),GetViewItemInlineKeyboardTemplate),\
                    GetAccess,\
                    default_keyboard_func,\
                    access_mode = user_access.AccessMode.VIEW\
                    )

class ModuleUserOrders(ModuleOrders):
    def __init__(self, a_ParentModName, a_ChildModName, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(table, messages, button_names, a_ParentModName, a_ChildModName, init_access, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)

    def GetName(self):
        return module_name
