# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Комментарии

from bot_sys import bot_bd, keyboard, user_access, user_messages, bd_table
from bot_modules import mod_table_operate, mod_simple_message

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMCreateComment(StatesGroup):
    name = State()
    desc = State()
    photo = State()
    
class FSMEditCommentPhotoItem(StatesGroup):
    item_field = State()

class FSMEditCommentNameItem(StatesGroup):
    item_field = State()

class FSMEditCommentDescItem(StatesGroup):
    item_field = State()

class FSMEditCommentAccessItem(StatesGroup):
    item_field = State()
# ---------------------------------------------------------
# БД
module_name = 'comments'

table_name = module_name
key_name = 'commentID'
name_field = 'commentName'
desc_field = 'commentDesc'
photo_field = 'commentPhoto'
access_field = 'commentAccess'
create_datetime_field = 'commentCreateDateTime'
parent_id_field = 'needID'

table = bd_table.Table(table_name, [
        bd_table.TableField(key_name, bd_table.TableFieldDestiny.KEY, bd_table.TableFieldType.INT),
        bd_table.TableField(name_field, bd_table.TableFieldDestiny.NAME, bd_table.TableFieldType.STR),
        bd_table.TableField(desc_field, bd_table.TableFieldDestiny.DESC, bd_table.TableFieldType.STR),
        bd_table.TableField(photo_field, bd_table.TableFieldDestiny.PHOTO, bd_table.TableFieldType.STR),
        bd_table.TableField(access_field, bd_table.TableFieldDestiny.ACCESS, bd_table.TableFieldType.STR),
        bd_table.TableField(create_datetime_field, bd_table.TableFieldDestiny.CREATE_DATE, bd_table.TableFieldType.STR),
        bd_table.TableField(parent_id_field, bd_table.TableFieldDestiny.PARENT_ID, bd_table.TableFieldType.INT),
        ])

init_access = f'{user_access.user_access_group_new}=va'

fsm = {
    mod_table_operate.FSMs.CREATE: FSMCreateComment,
    mod_table_operate.FSMs.EDIT_NAME: FSMEditCommentNameItem,
    mod_table_operate.FSMs.EDIT_DESC: FSMEditCommentDescItem,
    mod_table_operate.FSMs.EDIT_PHOTO: FSMEditCommentPhotoItem,
    mod_table_operate.FSMs.EDIT_ACCESS: FSMEditCommentAccessItem,
    }

# ---------------------------------------------------------
# Сообщения и кнопки

button_names = {
    mod_simple_message.ButtonNames.START: "⚏ Комментарии",
    mod_table_operate.ButtonNames.LIST: "📃 Список комментариев",
    mod_table_operate.ButtonNames.ADD: "☑ Добавить комментарий",
    mod_table_operate.ButtonNames.EDIT: "🛠 Редактировать комментарий",
    mod_table_operate.ButtonNames.EDIT_PHOTO: "☐ Изменить изображение у комментария",
    mod_table_operate.ButtonNames.EDIT_NAME: "≂ Изменить название у комментария",
    mod_table_operate.ButtonNames.EDIT_DESC: "𝌴 Изменить описание у комментария",
    mod_table_operate.ButtonNames.EDIT_ACCESS: "✋ Изменить доступ к комментарию",
    mod_table_operate.ButtonNames.DEL: "❌ Удалить комментарий",
}

messages = {
    mod_simple_message.Messages.START: f'''
<b>{button_names[mod_simple_message.ButtonNames.START]}</b>

''',
    mod_table_operate.Messages.SELECT: '''
Пожалуйста, выберите комментарий:
''',
    mod_table_operate.Messages.ERROR_FIND: '''
❌ Ошибка, комментарий не найден
''',
    mod_table_operate.Messages.OPEN: f'''
<b>Комментарий:  #{name_field}</b>

#{desc_field}

Время создания: #{create_datetime_field}
''',
    mod_table_operate.Messages.CREATE_NAME: '''
Создание комментария. Шаг №1

Введите название комментария:
''',
    mod_table_operate.Messages.CREATE_DESC: '''
Создание комментария. Шаг №2

Введите описание комментария:
''',
    mod_table_operate.Messages.CREATE_PHOTO: '''
Создание комментария. Шаг №3

Загрузите обложку для комментария (Фото):
Она будет отображаться в его описании.
''',
    mod_table_operate.Messages.SUCCESS_CREATE: '''✅ Комментарий успешно добавлен!''',
    mod_table_operate.Messages.START_EDIT: '''
Пожалуйста, выберите действие:
''',
    mod_table_operate.Messages.SELECT_TO_EDIT: '''
Выберите комментарий, который вы хотите отредактировать.
''',
    mod_table_operate.Messages.EDIT_PHOTO: '''
Загрузите новую обложку для комментария (Фото):
Она будет отображаться в его описании.
''',
    mod_table_operate.Messages.EDIT_NAME: f'''
Текущее название комментария:
#{name_field}

Введите новое название комментария:
''',
    mod_table_operate.Messages.EDIT_DESC: f'''
Текущее описание комментария:
#{desc_field}

Введите новое описание комментария:
''',
    mod_table_operate.Messages.EDIT_ACCESS: f'''
Текущий доступ к комментарийу:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
''',
    mod_table_operate.Messages.SUCCESS_EDIT: '''✅ Комментарий успешно отредактирован!''',
    mod_table_operate.Messages.SELECT_TO_DELETE: '''
Выберите комментарий, который вы хотите удалить.
''',
    mod_table_operate.Messages.SUCCESS_DELETE: '''✅ Комментарий успешно удалён!''',
}

class ModuleComments(mod_table_operate.TableOperateModule):
    def __init__(self, a_ParentModName, a_ChildModName, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(table, messages, button_names, fsm, a_ParentModName, a_ChildModName, init_access, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)

    def GetName(self):
        return module_name
