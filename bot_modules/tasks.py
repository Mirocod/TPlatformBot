# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Задачи

from bot_sys import bot_bd, keyboard, user_access, bd_table
from bot_modules import mod_table_operate, mod_simple_message

# ---------------------------------------------------------
# БД
module_name = 'tasks'

table_name = module_name
key_name = 'taskID'
name_field = 'taskName'
desc_field = 'taskDesc'
photo_field = 'taskPhoto'
access_field = 'taskAccess'
create_datetime_field = 'taskCreateDateTime'
parent_id_field = 'projectID'

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
    mod_simple_message.ButtonNames.START: "✎ Задачи",
    mod_table_operate.ButtonNames.LIST: "📃 Список задач",
    mod_table_operate.ButtonNames.ADD: "☑ Добавить задачу",
    mod_table_operate.ButtonNames.EDIT: "🛠 Редактировать задачу",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.PHOTO): "☐ Изменить изображение у задачи",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.NAME): "≂ Изменить название у задачи",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.DESC): "𝌴 Изменить описание у задачи",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.ACCESS): "✋ Изменить доступ к задаче",
    mod_table_operate.ButtonNames.DEL: "❌ Удалить задачу",
}

messages = {
    mod_simple_message.Messages.START: f'''
<b>{button_names[mod_simple_message.ButtonNames.START]}</b>

''',
    mod_table_operate.Messages.SELECT: '''
Пожалуйста, выберите задачу:
''',
    mod_table_operate.Messages.ERROR_FIND: '''
❌ Ошибка, задача не найдена
''',
    mod_table_operate.Messages.OPEN: f'''
<b>Задача:  #{name_field}</b>

#{desc_field}

Время создания: #{create_datetime_field}
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.NAME): '''
Создание задачи. Шаг №1

Введите название задачи:
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.DESC): '''
Создание задачи. Шаг №2

Введите описание задачи:
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.PHOTO): '''
Создание задачи. Шаг №3

Загрузите обложку для задачи (Фото):
Она будет отображаться в её описании.
''',
    mod_table_operate.Messages.SUCCESS_CREATE: '''✅ Задача успешно добавлена!''',
    mod_table_operate.Messages.START_EDIT: '''
Пожалуйста, выберите действие:
''',
    mod_table_operate.Messages.SELECT_TO_EDIT: '''
Выберите задачу, которую вы хотите отредактировать.
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.PHOTO): '''
Загрузите новую обложку для задачи (Фото):
Она будет отображаться в её описании.
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.NAME): f'''
Текущее название задачи:
#{name_field}

Введите новое название задачи:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.DESC): f'''
Текущее описание задачи:
#{desc_field}

Введите новое описание задачи:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.ACCESS): f'''
Текущий доступ к задаче:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
''',
    mod_table_operate.Messages.SUCCESS_EDIT: '''✅ Задача успешно отредактирован!''',
    mod_table_operate.Messages.SELECT_TO_DELETE: '''
Выберите задачу, которую вы хотите удалить.
Все потребности в этой задаче так же будут удалены!
''',
    mod_table_operate.Messages.SUCCESS_DELETE: '''✅ Задача успешно удалёна!''',
}

class ModuleTasks(mod_table_operate.TableOperateModule):
    def __init__(self, a_ParentModName, a_ChildModName, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(table, messages, button_names, a_ParentModName, a_ChildModName, init_access, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)

    def GetName(self):
        return module_name
