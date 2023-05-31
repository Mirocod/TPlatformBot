# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Заказы

from bot_sys import bot_bd, keyboard, user_access, bd_table
from bot_modules import mod_table_operate, mod_simple_message, orders
from template import bd_item_select, bd_item_view, bd_item


# ---------------------------------------------------------
# БД
module_name = 'all_orders'

table = orders.table

init_access = f'{user_access.user_access_group_new}=-'

# ---------------------------------------------------------
# Сообщения и кнопки

button_names = {}
button_names.update(orders.button_names)
button_names.pop(mod_table_operate.ButtonNames.ADD)

cur_button_names = {
    mod_simple_message.ButtonNames.START: "‍🛒 Все заказы",
    mod_table_operate.ButtonNames.LIST: "📃 Список текущих заказов",
    orders.ButtonNames.LIST_ALL: "📃 Список всех заказов",
    mod_table_operate.ButtonNames.EDIT: "🛠 Редактировать заказ",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.PHOTO): "☐ Изменить изображение в заказе",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.NAME): "≂ Изменить название в заказе",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.DESC): "𝌴 Изменить описание в заказе",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.ADDRESS): "𝌴 Изменить адрес в заказе",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.ACCESS): "✋ Изменить доступ к заказу",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.STATUS): "𝌴 Изменить статус в заказе",
    mod_table_operate.EnumButton(orders.OrderStatus.NEW): "Заказ ожидает модерации",
    mod_table_operate.EnumButton(orders.OrderStatus.PAY): "Заказ ожидает оплаты",
    mod_table_operate.EnumButton(orders.OrderStatus.ADDRESS): "Заказ ожидает уточнения адреса",
    mod_table_operate.EnumButton(orders.OrderStatus.FINISH): "Заказ выполнен",
    mod_table_operate.ButtonNames.DEL: "❌ Удалить заказ",}
button_names.update(cur_button_names)

messages = {}
messages.update(orders.messages)

cur_messages = {
    mod_simple_message.Messages.START: f'''
<b>{button_names[mod_simple_message.ButtonNames.START]}</b>

''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.STATUS): f'''
Текущий статус заказа:
#{orders.status_field}

Введите новый статус заказа:
''',
    mod_table_operate.Messages.OPEN: f'''
<b>Заказ: #{orders.name_field}</b>

<b>Описание и состав заказа:</b> #{orders.desc_field}

<b>Статус:</b> #{orders.status_field}

<b>Пользователь:</b> #{orders.parent_id_field}

<b>Адрес доставки:</b> #{orders.address_field}

<b>Время создания:</b> #{orders.create_datetime_field}
''',
}

messages.update(orders.messages_order_status)
messages.update(cur_messages)

def GetCurItemsTemplate(a_Bot, a_TableName, a_StatusFieldName):
    def GetBDItems(a_Message, a_UserGroups, a_ParentID):
        request = f'SELECT * FROM {a_TableName} WHERE {a_StatusFieldName} != ?'
        return a_Bot.SQLRequest(request, param = ([str(orders.OrderStatus.FINISH)]))
    return GetBDItems

def GetBDItemsForUserTemplate(a_Bot, a_TableName):
    def GetBDItems(a_Message, a_UserGroups, a_ParentID):
        return bd_item.GetAllItemsTemplate(a_Bot, a_TableName)()
    return GetBDItems

class DBItemForUserSelectSource(bd_item_select.DBItemSelectSource):
    def __init__(self, a_Bot, a_TableName, a_ParentIDFieldName, a_PrevPrefix, a_ButtonName, a_OnlyCurrent = False):
        super().__init__(a_Bot, a_TableName, a_ParentIDFieldName, a_PrevPrefix, a_ButtonName)
        self.m_OnlyCurrent = a_OnlyCurrent

    def GetItemsFunc(self):
        if self.m_OnlyCurrent:
            return GetCurItemsTemplate(self.m_Bot, self.m_TableName, orders.status_field)
        return GetBDItemsForUserTemplate(self.m_Bot, self.m_TableName)

    def IsFirst(self):
        return True

class ModuleAllOrders(orders.ModuleOrders):
    def __init__(self, a_ParentModName, a_ChildModName, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(table, messages, button_names, a_ParentModName, a_ChildModName, init_access, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)

    def GetInitBDCommands(self):
        # уже сделано в ModuleUserOrders
        return  []

    def GetName(self):
        return module_name

    def SelectSourceTemplate(self, a_PrevPrefix, a_ButtonName):
        parent_id_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PARENT_ID)
        return DBItemForUserSelectSource(self.m_Bot, self.m_Table.GetName(), parent_id_field, a_PrevPrefix, a_ButtonName, a_OnlyCurrent = True)

    def SelectSourceForAllTemplate(self, a_PrevPrefix, a_ButtonName):
        parent_id_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PARENT_ID)
        return DBItemForUserSelectSource(self.m_Bot, self.m_Table.GetName(), parent_id_field, a_PrevPrefix, a_ButtonName)

    def GetButtonNameAndKeyValueAndAccess(self, a_Item):
        parent_field_id = self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.PARENT_ID)
        n, k, a = super().GetButtonNameAndKeyValueAndAccess(a_Item)
        return n + ":" + str(a_Item[parent_field_id]), k, a
