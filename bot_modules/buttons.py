# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Сообщения

from bot_sys import bot_bd, keyboard, user_access, bd_table, bot_messages
from bot_modules import mod_table_operate, mod_simple_message, access_utils
from template import bd_item

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMCreateButton(StatesGroup):
    name = State()
    desc = State()
    photo = State()
    
class FSMEditButtonPhotoItem(StatesGroup):
    item_id = State()
    item_field = State()

class FSMEditButtonNameItem(StatesGroup):
    item_id = State()
    item_field = State()

class FSMEditButtonDescItem(StatesGroup):
    item_id = State()
    item_field = State()

class FSMEditButtonAccessItem(StatesGroup):
    item_id = State()
    item_field = State()
# ---------------------------------------------------------
# БД
module_name = 'buttons'

table_name = module_name
key_name = 'buttonID'
name_field = 'buttonName'
desc_field = 'buttonDesc'
photo_field = 'buttonPhoto'
access_field = 'buttonAccess'
create_datetime_field = 'buttonCreateDateTime'
parent_id_field = 'languageID'

table_name_field = bd_table.TableField(name_field, bd_table.TableFieldDestiny.NAME, bd_table.TableFieldType.STR)
table_parent_id_field = bd_table.TableField(parent_id_field, bd_table.TableFieldDestiny.PARENT_ID, bd_table.TableFieldType.INT)

table = bd_table.Table(table_name, [
        bd_table.TableField(key_name, bd_table.TableFieldDestiny.KEY, bd_table.TableFieldType.INT),
        table_name_field,
        bd_table.TableField(desc_field, bd_table.TableFieldDestiny.DESC, bd_table.TableFieldType.STR),
        bd_table.TableField(photo_field, bd_table.TableFieldDestiny.PHOTO, bd_table.TableFieldType.STR),
        bd_table.TableField(access_field, bd_table.TableFieldDestiny.ACCESS, bd_table.TableFieldType.STR),
        bd_table.TableField(create_datetime_field, bd_table.TableFieldDestiny.CREATE_DATE, bd_table.TableFieldType.STR),
        table_parent_id_field,
        ],
        [
            [table_name_field, table_parent_id_field],
        ]
)

init_access = f'{user_access.user_access_group_all}=-'

fsm = {
    mod_table_operate.FSMs.CREATE: FSMCreateButton,
    mod_table_operate.FSMs.EDIT_NAME: FSMEditButtonNameItem,
    mod_table_operate.FSMs.EDIT_DESC: FSMEditButtonDescItem,
    mod_table_operate.FSMs.EDIT_PHOTO: FSMEditButtonPhotoItem,
    mod_table_operate.FSMs.EDIT_ACCESS: FSMEditButtonAccessItem,
    }

# ---------------------------------------------------------
# Сообщения и кнопки

button_names = {
    mod_simple_message.ButtonNames.START: "❍ Названия кнопок",
    mod_table_operate.ButtonNames.LIST: "📃 Список названий кнопок",
    mod_table_operate.ButtonNames.ADD: "☑ Добавить название кнопки",
    mod_table_operate.ButtonNames.EDIT: "🛠 Редактировать названия кнопок",
    mod_table_operate.ButtonNames.EDIT_PHOTO: "☐ Изменить изображение у названия кнопок",
    mod_table_operate.ButtonNames.EDIT_NAME: "≂ Изменить название у названия кнопок",
    mod_table_operate.ButtonNames.EDIT_DESC: "𝌴 Изменить описание у названия кнопок",
    mod_table_operate.ButtonNames.EDIT_ACCESS: "✋ Изменить доступ к названию кнопки",
    mod_table_operate.ButtonNames.DEL: "❌ Удалить название кнопки",
}

messages = {
    mod_simple_message.Messages.START: f'''
<b>{button_names[mod_simple_message.ButtonNames.START]}</b>

''',
    mod_table_operate.Messages.SELECT: '''
Пожалуйста, выберите название кнопки:
''',
    mod_table_operate.Messages.ERROR_FIND: '''
❌ Ошибка, название кнопки не найдено
''',
    mod_table_operate.Messages.OPEN: f'''
<b>Название кнопки:  #{name_field}</b>

#{desc_field}

Время создания: #{create_datetime_field}
''',
    mod_table_operate.Messages.CREATE_NAME: '''
Создание названия кнопки Шаг №1

Введите название название кнопки:
''',
    mod_table_operate.Messages.CREATE_DESC: '''
Создание названия кнопки. Шаг №2

Введите описание название кнопки:
''',
    mod_table_operate.Messages.CREATE_PHOTO: '''
Создание названия кнопки
Загрузите обложку для названия кнопок (Фото):
На данный момент не поддерживается!
Нажмите пропустить
''',
    mod_table_operate.Messages.SUCCESS_CREATE: '''✅ Название кнопки успешно добавлено!''',
    mod_table_operate.Messages.START_EDIT: '''
Пожалуйста, выберите действие:
''',
    mod_table_operate.Messages.SELECT_TO_EDIT: '''
Выберите название кнопки, который вы хотите отредактировать.
''',
    mod_table_operate.Messages.EDIT_PHOTO: '''
Загрузите новую обложку для названия кнопок (Фото):
Она будет отображаться в его описании.
''',
    mod_table_operate.Messages.EDIT_NAME: f'''
Текущее название названия кнопок:
#{name_field}

Введите новое название названия кнопки:
''',
    mod_table_operate.Messages.EDIT_DESC: f'''
Текущее описание названия кнопок:
#{desc_field}

Введите новое описание названия кнопки:
''',
    mod_table_operate.Messages.EDIT_ACCESS: f'''
Текущий доступ к названию кнопки:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
''',
    mod_table_operate.Messages.SUCCESS_EDIT: '''✅ Название кнопки успешно отредактировано!''',
    mod_table_operate.Messages.SELECT_TO_DELETE: '''
Выберите название кнопки, которое вы хотите удалить.
''',
    mod_table_operate.Messages.SUCCESS_DELETE: '''✅ Название кнопки успешно удалено!''',
}

class ModuleButtons(mod_table_operate.TableOperateModule):
    def __init__(self, a_ParentModName, a_ChildModName, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(table, messages, button_names, fsm, a_ParentModName, a_ChildModName, init_access, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)

    def GetName(self):
        return module_name

    def AddOrIgnoreMessage(self, a_Message):
        table_name = self.m_Table.GetName()
        name_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.NAME)
        photo_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PHOTO)
        desc_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.DESC)
        access_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.ACCESS)
        create_datetime_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.CREATE_DATE)
        parent_id_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PARENT_ID)

        lang_id = self.GetModule(self.m_ParentModName).GetLangID(a_Message.m_Language)
        return self.m_Bot.SQLRequest(f'INSERT OR IGNORE INTO {table_name}({photo_field}, {name_field}, {desc_field}, {access_field}, {parent_id_field}, {create_datetime_field}) VALUES(?, ?, ?, ?, ?, {bot_bd.GetBDDateTimeNow()})', 
                commit = True, return_error = True, param = (a_Message.m_PhotoID, a_Message.m_MessageName, a_Message.m_MessageDesc, access_utils.GetItemDefaultAccessForModule(self.m_Bot, module_name), lang_id))

    def FlushMessages(self):
        msg = self.m_BotButtons.GetMessages()
        for lang, msg_dict in msg.items():
            for msg_name, message in msg_dict.items():
                self.AddOrIgnoreMessage(message)

        table_name = self.m_Table.GetName()
        msgs_bd = bd_item.GetAllItemsTemplate(self.m_Bot, table_name)()
        if msgs_bd:
            for m in msgs_bd:
                name = m[1]
                desc = m[2]
                photo_id = m[3]
                lang_id = m[6]
                lang_name = self.GetModule(self.m_ParentModName).GetLangName(lang_id)
                self.m_BotButtons.CreateMessage(name, desc, self.m_Log.GetTimeNow(), a_MessagePhotoID = photo_id, a_MessageLang = lang_name)

        self.m_BotButtons.UpdateSignal(self.m_Log.GetTimeNow())

    def OnChange(self):
        self.FlushMessages()
