# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Проекты

from bot_sys import bot_bd, keyboard, user_access, bd_table
from bot_modules import mod_table_operate, mod_simple_message

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMCreateProject(StatesGroup):
    name = State()
    desc = State()
    photo = State()
    
class FSMEditProjectPhotoItem(StatesGroup):
    item_field = State()

class FSMEditProjectNameItem(StatesGroup):
    item_field = State()

class FSMEditProjectDescItem(StatesGroup):
    item_field = State()

class FSMEditProjectAccessItem(StatesGroup):
    item_field = State()
# ---------------------------------------------------------
# БД
module_name = 'projects'

table_name = module_name
key_name = 'projectID'
name_field = 'projectName'
desc_field = 'projectDesc'
photo_field = 'projectPhoto'
access_field = 'projectAccess'
create_datetime_field = 'projectCreateDateTime'

table = bd_table.Table(table_name, [
        bd_table.TableField(key_name, bd_table.TableFieldDestiny.KEY, bd_table.TableFieldType.INT),
        bd_table.TableField(name_field, bd_table.TableFieldDestiny.NAME, bd_table.TableFieldType.STR),
        bd_table.TableField(desc_field, bd_table.TableFieldDestiny.DESC, bd_table.TableFieldType.STR),
        bd_table.TableField(photo_field, bd_table.TableFieldDestiny.PHOTO, bd_table.TableFieldType.STR),
        bd_table.TableField(access_field, bd_table.TableFieldDestiny.ACCESS, bd_table.TableFieldType.STR),
        bd_table.TableField(create_datetime_field, bd_table.TableFieldDestiny.CREATE_DATE, bd_table.TableFieldType.STR),
        ])

init_access = f'{user_access.user_access_group_new}=va'

fsm = {
    mod_table_operate.FSMs.CREATE: FSMCreateProject,
    mod_table_operate.FSMs.EDIT_NAME: FSMEditProjectNameItem,
    mod_table_operate.FSMs.EDIT_DESC: FSMEditProjectDescItem,
    mod_table_operate.FSMs.EDIT_PHOTO: FSMEditProjectPhotoItem,
    mod_table_operate.FSMs.EDIT_ACCESS: FSMEditProjectAccessItem,
    }

# ---------------------------------------------------------
# Сообщения и кнопки

button_names = {
    mod_simple_message.ButtonNames.START: "🟥 Проекты",
    mod_table_operate.ButtonNames.LIST: "📃 Список проектов",
    mod_table_operate.ButtonNames.ADD: "✅ Добавить проект",
    mod_table_operate.ButtonNames.EDIT: "🛠 Редактировать проект",
    mod_table_operate.ButtonNames.EDIT_PHOTO: "☐ Изменить изображение в проекте",
    mod_table_operate.ButtonNames.EDIT_NAME: "≂ Изменить название в проекте",
    mod_table_operate.ButtonNames.EDIT_DESC: "𝌴 Изменить описание в проекте",
    mod_table_operate.ButtonNames.EDIT_ACCESS: "✋ Изменить доступ к проекту",
    mod_table_operate.ButtonNames.DEL: "❌ Удалить проект",
}

messages = {
    mod_simple_message.Messages.START: f'''
<b>{button_names[mod_simple_message.ButtonNames.START]}</b>

''',
    mod_table_operate.Messages.SELECT: '''
Пожалуйста, выберите проект:
''',
    mod_table_operate.Messages.ERROR_FIND: '''
❌ Ошибка, проект не найден
''',
    mod_table_operate.Messages.OPEN: f'''
<b>Проект:  #{name_field}</b>

#{desc_field}

Время создания: #{create_datetime_field}
''',
    mod_table_operate.Messages.CREATE_NAME: '''
Создание проекта. Шаг №1

Введите название проекта:
''',
    mod_table_operate.Messages.CREATE_DESC: '''
Создание проекта. Шаг №2

Введите описание проекта:
''',
    mod_table_operate.Messages.CREATE_PHOTO: '''
Создание проекта. Шаг №3

Загрузите обложку для проекта (Фото):
Она будет отображаться в его описании.
''',
    mod_table_operate.Messages.SUCCESS_CREATE: '''✅ Проект успешно добавлен!''',
    mod_table_operate.Messages.START_EDIT: '''
Пожалуйста, выберите действие:
''',
    mod_table_operate.Messages.SELECT_TO_EDIT: '''
Выберите проект, который вы хотите отредактировать.
''',
    mod_table_operate.Messages.EDIT_PHOTO: '''
Загрузите новую обложку для проекта (Фото):
Она будет отображаться в его описании.
''',
    mod_table_operate.Messages.EDIT_NAME: f'''
Текущее название проекта:
#{name_field}

Введите новое название проекта:
''',
    mod_table_operate.Messages.EDIT_DESC: f'''
Текущее описание проекта:
#{desc_field}

Введите новое описание проекта:
''',
    mod_table_operate.Messages.EDIT_ACCESS: f'''
Текущий доступ к проекту:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
''',
    mod_table_operate.Messages.SUCCESS_EDIT: '''✅ Проект успешно отредактирован!''',
    mod_table_operate.Messages.SELECT_TO_DELETE: '''
Выберите проект, который вы хотите удалить.
Все задачи и потребности в этом проекте так же будут удалены!
''',
    mod_table_operate.Messages.SUCCESS_DELETE: '''✅ Проект успешно удалён!''',
}

class ModuleProjects(mod_table_operate.TableOperateModule):
    def __init__(self, a_ParentModName, a_ChildModName, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(table, messages, button_names, fsm, a_ParentModName, a_ChildModName, init_access, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)

    def GetName(self):
        return module_name

    def GetModuleButtons(self):
        return super().GetModuleButtons() + [
                keyboard.ButtonWithAccess(self.GetButton(mod_table_operate.ButtonNames.LIST), user_access.AccessMode.VIEW, self.GetAccess()),
                ]


