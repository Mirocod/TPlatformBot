# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Группы

from bot_sys import bot_bd, keyboard, user_access, bd_table
from bot_modules import mod_table_operate, mod_simple_message
from bot_modules import access_utils, groups_utils

# ---------------------------------------------------------
# БД
module_name = 'groups'

table_name = groups_utils.table_name
key_name = groups_utils.key_name
name_field = groups_utils.name_field
desc_field = groups_utils.desc_field
photo_field = groups_utils.photo_field
access_field = groups_utils.access_field
create_datetime_field = groups_utils.create_datetime_field

table_name_field = bd_table.TableField(name_field, bd_table.TableFieldDestiny.NAME, bd_table.TableFieldType.STR)

table = bd_table.Table(table_name, [
        bd_table.TableField(key_name, bd_table.TableFieldDestiny.KEY, bd_table.TableFieldType.INT),
        table_name_field,
        bd_table.TableField(desc_field, bd_table.TableFieldDestiny.DESC, bd_table.TableFieldType.STR),
        bd_table.TableField(photo_field, bd_table.TableFieldDestiny.PHOTO, bd_table.TableFieldType.PHOTO),
        bd_table.TableField(access_field, bd_table.TableFieldDestiny.ACCESS, bd_table.TableFieldType.STR),
        bd_table.TableField(create_datetime_field, bd_table.TableFieldDestiny.CREATE_DATE, bd_table.TableFieldType.STR),
        ],
        [
            [table_name_field],
        ]
        )

init_access = f'{user_access.user_access_group_new}=-'

# ---------------------------------------------------------
# Сообщения и кнопки

button_names = {
    mod_simple_message.ButtonNames.START: "👥 Группы пользователей",
    mod_table_operate.ButtonNames.LIST: "📃 Список групп",
    mod_table_operate.ButtonNames.ADD: "✅ Добавить группу",
    mod_table_operate.ButtonNames.EDIT: "🛠 Редактировать группу",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.PHOTO): "☐ Изменить изображение в группе",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.NAME): "≂ Изменить название в группе",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.DESC): "𝌴 Изменить описание в группе",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.ACCESS): "✋ Изменить доступ к группе",
    mod_table_operate.ButtonNames.DEL: "❌ Удалить группу",
}

messages = {
    mod_simple_message.Messages.START: f'''
<b>{button_names[mod_simple_message.ButtonNames.START]}</b>

''',
    mod_table_operate.Messages.SELECT: '''
Пожалуйста, выберите группу:
''',
    mod_table_operate.Messages.ERROR_FIND: '''
❌ Ошибка, группу не найден
''',
    mod_table_operate.Messages.OPEN: f'''
<b>Группа:  #{name_field}</b>

#{desc_field}

Время создания: #{create_datetime_field}
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.NAME): '''
Создание группы. Шаг №1

Введите название группы:
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.DESC): '''
Создание группы. Шаг №2

Введите описание группы:
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.PHOTO): '''
Создание группы. Шаг №3

Загрузите обложку для группы (Фото):
Она будет отображаться в его описании.
''',
    mod_table_operate.Messages.SUCCESS_CREATE: '''✅ Группа успешно добавлена!''',
    mod_table_operate.Messages.START_EDIT: '''
Пожалуйста, выберите действие:
''',
    mod_table_operate.Messages.SELECT_TO_EDIT: '''
Выберите группу, которого вы хотите отредактировать.
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.PHOTO): '''
Загрузите новую обложку для группы (Фото):
Она будет отображаться в его описании.
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.NAME): f'''
Текущее название группы:
#{name_field}

Введите новое название группы:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.DESC): f'''
Текущее описание группы:
#{desc_field}

Введите новое описание группы:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.ACCESS): f'''
Текущий доступ к группе:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
''',
    mod_table_operate.Messages.SUCCESS_EDIT: '''✅ Группа успешно отредактирована!''',
    mod_table_operate.Messages.SELECT_TO_DELETE: '''
Выберите группу, который вы хотите удалить.
''',
    mod_table_operate.Messages.SUCCESS_DELETE: '''✅ Группа успешно удалена!''',
}

class ModuleGroups(mod_table_operate.TableOperateModule):
    def __init__(self, a_ParentModName, a_ChildModName, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_BotSubscribes, a_Log):
        super().__init__(table, messages, button_names, a_ParentModName, a_ChildModName, init_access, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_BotSubscribes, a_Log)

    def GetName(self):
        return module_name

    def GetInitBDCommands(self):
        return super(). GetInitBDCommands() + [
            f"INSERT OR IGNORE INTO {table_name} ({name_field}, {access_field}, {create_datetime_field}) VALUES ('{user_access.user_access_group_new}', '{user_access.user_access_group_new}=-', {bot_bd.GetBDDateTimeNow()});"
            ]
