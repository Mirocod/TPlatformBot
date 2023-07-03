# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Потребности

from bot_sys import bot_bd, keyboard, user_access, bd_table, bot_subscribes
from bot_modules import mod_table_operate, mod_simple_message

# ---------------------------------------------------------
# БД
module_name = 'needs'

table_name = module_name
key_name = 'needID'
name_field = 'needName'
desc_field = 'needDesc'
photo_field = 'needPhoto'
access_field = 'needAccess'
create_datetime_field = 'needCreateDateTime'
parent_id_field = 'taskID'

table = bd_table.Table(table_name, [
        bd_table.TableField(key_name, bd_table.TableFieldDestiny.KEY, bd_table.TableFieldType.INT),
        bd_table.TableField(name_field, bd_table.TableFieldDestiny.NAME, bd_table.TableFieldType.STR),
        bd_table.TableField(desc_field, bd_table.TableFieldDestiny.DESC, bd_table.TableFieldType.STR),
        bd_table.TableField(photo_field, bd_table.TableFieldDestiny.PHOTO, bd_table.TableFieldType.PHOTO),
        bd_table.TableField(access_field, bd_table.TableFieldDestiny.ACCESS, bd_table.TableFieldType.STR),
        bd_table.TableField(create_datetime_field, bd_table.TableFieldDestiny.CREATE_DATE, bd_table.TableFieldType.STR),
        bd_table.TableField(parent_id_field, bd_table.TableFieldDestiny.PARENT_ID, bd_table.TableFieldType.INT),
        ])

init_access = f'{user_access.user_access_group_new}=va'

# ---------------------------------------------------------
# Сообщения и кнопки

button_names = {
    mod_simple_message.ButtonNames.START: "👉 Потребности",
    mod_table_operate.ButtonNames.LIST: "📃 Список потребностей",
    mod_table_operate.ButtonNames.ADD: "☑ Добавить потребность",
    mod_table_operate.ButtonNames.EDIT: "🛠 Редактировать потребность",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.PHOTO): "☐ Изменить изображение у потребности",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.NAME): "≂ Изменить название у потребности",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.DESC): "𝌴 Изменить описание у потребности",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.ACCESS): "✋ Изменить доступ к потребности",
    mod_table_operate.ButtonNames.DEL: "❌ Удалить потребность",
}

messages = {
    mod_simple_message.Messages.START: f'''
<b>{button_names[mod_simple_message.ButtonNames.START]}</b>

''',
    mod_table_operate.Messages.SELECT: '''
Пожалуйста, выберите потребность:
''',
    mod_table_operate.Messages.ERROR_FIND: '''
❌ Ошибка, потребность не найдена
''',
    mod_table_operate.Messages.OPEN: f'''
<b>Потребность:  #{name_field}</b>

#{desc_field}

Время создания: #{create_datetime_field}
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.NAME): '''
Создание потребности. Шаг №1

Введите название потребности:
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.DESC): '''
Создание потребности. Шаг №2

Введите описание потребности:
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.PHOTO): '''
Создание потребности. Шаг №3

Загрузите обложку для потребности (Фото):
Она будет отображаться в её описании.
''',
    mod_table_operate.Messages.SUCCESS_CREATE: '''✅ Потребность успешно добавлена!''',
    mod_table_operate.Messages.START_EDIT: '''
Пожалуйста, выберите действие:
''',
    mod_table_operate.Messages.SELECT_TO_EDIT: '''
Выберите потребность, которую вы хотите отредактировать.
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.PHOTO): '''
Загрузите новую обложку для потребности (Фото):
Она будет отображаться в её описании.
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.NAME): f'''
Текущее название потребности:
#{name_field}

Введите новое название потребности:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.DESC): f'''
Текущее описание потребности:
#{desc_field}

Введите новое описание потребности:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.ACCESS): f'''
Текущий доступ к потребности:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
''',
    mod_table_operate.Messages.SUCCESS_EDIT: '''✅ Потребность успешно отредактирован!''',
    mod_table_operate.Messages.SELECT_TO_DELETE: '''
Выберите потребность, которую вы хотите удалить.
Все комментарии в этой потребности так же будут удалены!
''',
    mod_table_operate.Messages.SUCCESS_DELETE: '''✅ Потребность успешно удалёна!''',
}

messages_subscribes = {
    mod_table_operate.SubscribeMessage(bot_subscribes.SubscribeType.ADD):f'''Потребность создана''',
    mod_table_operate.SubscribeMessage(bot_subscribes.SubscribeType.ANY_ITEM_EDIT):f'''Потребность отредактирована''',
    mod_table_operate.SubscribeMessage(bot_subscribes.SubscribeType.ANY_ITEM_DEL):f'''Потребность удалёна''',
    mod_table_operate.SubscribeMessage(bot_subscribes.SubscribeType.ITEM_EDIT):f'''Потребность отредактирована #item_id''',
    mod_table_operate.SubscribeMessage(bot_subscribes.SubscribeType.ITEM_DEL):f'''Потребность удалёна #item_id''',
}

messages.update(messages_subscribes)

class ModuleNeeds(mod_table_operate.TableOperateModule):
    def __init__(self, a_ParentModName, a_ChildModName, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_BotSubscribes, a_Log):
        super().__init__(table, messages, button_names, a_ParentModName, a_ChildModName, init_access, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_BotSubscribes, a_Log)

    def GetName(self):
        return module_name
