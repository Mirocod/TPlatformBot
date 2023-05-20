# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Языки

from bot_sys import bot_bd, keyboard, user_access, user_messages, bd_table
from bot_modules import mod_table_operate, mod_simple_message, access_utils
from template import bd_item

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMCreateLanguage(StatesGroup):
    name = State()
    desc = State()
    photo = State()
    
class FSMEditLanguagePhotoItem(StatesGroup):
    item_field = State()

class FSMEditLanguageNameItem(StatesGroup):
    item_field = State()

class FSMEditLanguageDescItem(StatesGroup):
    item_field = State()

class FSMEditLanguageAccessItem(StatesGroup):
    item_field = State()
# ---------------------------------------------------------
# БД
module_name = 'languages'

table_name = module_name
key_name = 'languageID'
name_field = 'languageName'
desc_field = 'languageDesc'
photo_field = 'languagePhoto'
access_field = 'languageAccess'
create_datetime_field = 'languageCreateDateTime'

table_name_field = bd_table.TableField(name_field, bd_table.TableFieldDestiny.NAME, bd_table.TableFieldType.STR)

table = bd_table.Table(table_name, [
        bd_table.TableField(key_name, bd_table.TableFieldDestiny.KEY, bd_table.TableFieldType.INT),
        table_name_field,
        bd_table.TableField(desc_field, bd_table.TableFieldDestiny.DESC, bd_table.TableFieldType.STR),
        bd_table.TableField(photo_field, bd_table.TableFieldDestiny.PHOTO, bd_table.TableFieldType.STR),
        bd_table.TableField(access_field, bd_table.TableFieldDestiny.ACCESS, bd_table.TableFieldType.STR),
        bd_table.TableField(create_datetime_field, bd_table.TableFieldDestiny.CREATE_DATE, bd_table.TableFieldType.STR),
        ],
        [
            [table_name_field],
        ]
)

init_access = f'{user_access.user_access_group_all}=-'

fsm = {
    mod_table_operate.FSMs.CREATE: FSMCreateLanguage,
    mod_table_operate.FSMs.EDIT_NAME: FSMEditLanguageNameItem,
    mod_table_operate.FSMs.EDIT_DESC: FSMEditLanguageDescItem,
    mod_table_operate.FSMs.EDIT_PHOTO: FSMEditLanguagePhotoItem,
    mod_table_operate.FSMs.EDIT_ACCESS: FSMEditLanguageAccessItem,
    }

# ---------------------------------------------------------
# Сообщения и кнопки

button_names = {
    mod_simple_message.ButtonNames.START: "⚑ Языки",
    mod_table_operate.ButtonNames.LIST: "📃 Список языков",
    mod_table_operate.ButtonNames.ADD: "✅ Добавить язык",
    mod_table_operate.ButtonNames.EDIT: "🛠 Редактировать язык",
    mod_table_operate.ButtonNames.EDIT_PHOTO: "☐ Изменить изображение в языке",
    mod_table_operate.ButtonNames.EDIT_NAME: "≂ Изменить название в языке",
    mod_table_operate.ButtonNames.EDIT_DESC: "𝌴 Изменить описание в языке",
    mod_table_operate.ButtonNames.EDIT_ACCESS: "✋ Изменить доступ к языку",
    mod_table_operate.ButtonNames.DEL: "❌ Удалить язык",
}

messages = {
    mod_simple_message.Messages.START: f'''
<b>{button_names[mod_simple_message.ButtonNames.START]}</b>

''',
    mod_table_operate.Messages.SELECT: '''
Пожалуйста, выберите язык:
''',
    mod_table_operate.Messages.ERROR_FIND: '''
❌ Ошибка, язык не найден
''',
    mod_table_operate.Messages.OPEN: f'''
<b>Язык:  #{name_field}</b>

#{desc_field}

Время создания: #{create_datetime_field}
''',
    mod_table_operate.Messages.CREATE_NAME: '''
Создание языка. Шаг №1

Введите название языка:
''',
    mod_table_operate.Messages.CREATE_DESC: '''
Создание языка. Шаг №2

Введите описание языка:
''',
    mod_table_operate.Messages.CREATE_PHOTO: '''
Создание языка. Шаг №3

Загрузите обложку для языка (Фото):
Она будет отображаться в его описании.
''',
    mod_table_operate.Messages.SUCCESS_CREATE: '''✅ Язык успешно добавлен!''',
    mod_table_operate.Messages.START_EDIT: '''
Пожалуйста, выберите действие:
''',
    mod_table_operate.Messages.SELECT_TO_EDIT: '''
Выберите язык, который вы хотите отредактировать.
''',
    mod_table_operate.Messages.EDIT_PHOTO: '''
Загрузите новую обложку для языка (Фото):
Она будет отображаться в его описании.
''',
    mod_table_operate.Messages.EDIT_NAME: f'''
Текущее название языка:
#{name_field}

Введите новое название языка:
''',
    mod_table_operate.Messages.EDIT_DESC: f'''
Текущее описание языка:
#{desc_field}

Введите новое описание языка:
''',
    mod_table_operate.Messages.EDIT_ACCESS: f'''
Текущий доступ к языку:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
''',
    mod_table_operate.Messages.SUCCESS_EDIT: '''✅ Язык успешно отредактирован!''',
    mod_table_operate.Messages.SELECT_TO_DELETE: '''
Выберите язык, который вы хотите удалить.
Все задачи и потребности в этом языке так же будут удалены!
''',
    mod_table_operate.Messages.SUCCESS_DELETE: '''✅ Язык успешно удалён!''',
}

class ModuleLanguages(mod_table_operate.TableOperateModule):
    def __init__(self, a_ParentModName, a_ChildModName, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(table, messages, button_names, fsm, a_ParentModName, a_ChildModName, init_access, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)
        self.m_LanguageIDs = {}

    def GetName(self):
        return module_name

    def GetLangID(self, a_Lang):
        return self.m_LanguageIDs.get(a_Lang, None)

    def GetLangName(self, a_LangID):
        for lang_name, lang_id in self.m_LanguageIDs:
            if a_LangID == lang_id:
                return lang_name
        return user_messages.default_language

    def FlushLanguages(self):
        msg = self.m_BotMessages.GetMessages()
        for lang, msg_dict in msg.items():
            self.AddOrIgnoreLang(lang)
        langs = bd_item.GetAllItemsTemplate(self.m_Bot, table_name)()
        if langs:
            for l in langs:
                self.m_LanguageIDs[l[1]] = str(l[0])
        print('FlushLanguages', self.m_LanguageIDs)

    def AddOrIgnoreLang(self, a_Lang : str):
        table_name = self.m_Table.GetName()
        name_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.NAME)
        photo_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PHOTO)
        desc_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.DESC)
        access_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.ACCESS)
        create_datetime_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.CREATE_DATE)

        res, error = self.m_Bot.SQLRequest(f'INSERT OR IGNORE INTO {table_name}({photo_field}, {name_field}, {desc_field}, {access_field}, {create_datetime_field}) VALUES(?, ?, ?, ?, {bot_bd.GetBDDateTimeNow()})', 
                commit = True, return_error = True, param = (0, a_Lang, '', access_utils.GetItemDefaultAccessForModule(self.m_Bot, module_name)))

    def OnChange(self):
        self.FlushLanguages()

'''
# стартовое язык
async def LanguagesOpen(a_Language : types.message, state = None):
    return simple_message.WorkFuncResult(base_language_message)

def GetButtonNameAndKeyValueAndAccess(a_Item):
    # languageName languageID languageAccess
    return a_Item[1], a_Item[0], a_Item[4]

def ShowMessageTemplate(a_StringLanguage, keyboard_template_func = None):
    async def ShowLanguage(a_CallbackQuery : types.CallbackQuery, a_Item):
        if (len(a_Item) < 6):
            return simple_message.WorkFuncResult(error_find_proj_message)

        msg = a_StringLanguage.\
                replace(f'#{name_field}', a_Item[1]).\
                replace(f'#{desc_field}', a_Item[2]).\
                replace(f'#{create_datetime_field}', a_Item[5]).\
                replace(f'#{access_field}', a_Item[4])
        keyboard_func = None
        if keyboard_template_func:
            keyboard_func = keyboard_template_func(a_Item[0])
        return simple_message.WorkFuncResult(msg, photo_id = a_Item[3], item_access = a_Item[4], keyboard_func = keyboard_func)
    return ShowLanguage

def SimpleMessageTemplateLegacy(a_StringLanguage):
    async def ShowLanguage(a_CallbackQuery : types.CallbackQuery, a_Item):
        return simple_message.WorkFuncResult(a_StringLanguage)
    return ShowLanguage

# Удаление языка 

async def LanguagePreDelete(a_CallbackQuery : types.CallbackQuery, a_Item):
    if (len(a_Item) < 6):
        return simple_message.WorkFuncResult(error_find_proj_message)
    access = a_Item[4]
    return simple_message.WorkFuncResult('', None, item_access = access)

async def LanguagePostDelete(a_CallbackQuery : types.CallbackQuery, a_ItemID):
    log.Success(f'Язык №{a_ItemID} был удалён пользователем {a_CallbackQuery.from_user.id}.')
    #TODO: удалить вложенные 
    FlushLanguages()
    return simple_message.WorkFuncResult(language_success_delete_message)

# ---------------------------------------------------------
# Работа с базой данных языков

def AddBDItemFunc(a_ItemData, a_UserID):
    res, error = bot_bd.SQLRequestToBD(f'INSERT INTO {table_name}({photo_field}, {name_field}, {desc_field}, {access_field}, {create_datetime_field}) VALUES(?, ?, ?, ?, {bot_bd.GetBDDateTimeNow()})', 
            commit = True, return_error = True, param = (a_ItemData[photo_field], a_ItemData[name_field], a_ItemData[desc_field], access.GetItemDefaultAccessForModule(module_name) + f";{a_UserID}=+"))

    if error:
        log.Error(f'Пользоватлель {a_UserID}. Ошибка добавления записи в таблицу {table_name} ({a_ItemData[photo_field]}, {a_ItemData[name_field]}, {a_ItemData[desc_field]}, {access.GetItemDefaultAccessForModule(module_name)}).')
    else:
        log.Success(f'Пользоватлель {a_UserID}. Добавлена запись в таблицу {table_name} ({a_ItemData[photo_field]}, {a_ItemData[name_field]}, {a_ItemData[desc_field]}, {access.GetItemDefaultAccessForModule(module_name)}).')

    FlushLanguages()
    return res, error

# ---------------------------------------------------------
# API

def AddOrIgnoreLang(a_Lang : str):
    res, error = bot_bd.SQLRequestToBD(f'INSERT OR IGNORE INTO {table_name}({photo_field}, {name_field}, {desc_field}, {access_field}, {create_datetime_field}) VALUES(?, ?, ?, ?, {bot_bd.GetBDDateTimeNow()})', 
            commit = True, return_error = True, param = (0, a_Lang, '', access.GetItemDefaultAccessForModule(module_name)))

m_LanguageIDs = {}
def GetLangID(a_Lang):
    global m_LanguageIDs
    return m_LanguageIDs.get(a_Lang, None)

def GetLangName(a_LangID):
    global m_LanguageIDs
    for lang_name, lang_id in m_LanguageIDs:
        if a_LangID == lang_id:
            return lang_name
    return user_messages.default_language

def FlushLanguages():
    global m_LanguageIDs
    msg = user_messages.GetMessages()
    for lang, msg_dict in msg.items():
        AddOrIgnoreLang(lang)
    langs = bd_item.GetAllItemsTemplate(table_name)()
    if langs:
        for l in langs:
            m_LanguageIDs[l[1]] = str(l[0])
    print('FlushLanguages', m_LanguageIDs)

# Инициализация БД
def GetInitBDCommands():
    return init_bd_cmds

def GetAccess():
    return access.GetAccessForModule(module_name)

# Доступные кнопки
def GetModuleButtons():
    return [
            keyboard.ButtonWithAccess(languages_button_name, user_access.AccessMode.VIEW, GetAccess()),
            ]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    defaul_keyboard_func = GetStartLanguageKeyboardButtons

    # Список языков
    dp.register_message_handler(simple_message.SimpleMessageTemplateLegacy(LanguagesOpen, defaul_keyboard_func, GetAccess), text = languages_button_name)
    bd_item_view.FirstSelectAndShowBDItemRegisterHandlers(dp, \
            list_language_button_name, \
            table_name, \
            key_name, \
            ShowMessageTemplate(language_open_message, GetViewItemInlineKeyboardTemplate), \
            GetButtonNameAndKeyValueAndAccess, \
            select_language_message, \
            GetAccess, \
            defaul_keyboard_func\
            )

    # Удаление языка
    bd_item_delete.DeleteBDItemRegisterHandlers(dp, \
            None, \
            bd_item.GetCheckForTextFunc(del_language_button_name), \
            table_name, \
            key_name, \
            None, \
            LanguagePreDelete, \
            LanguagePostDelete, \
            GetButtonNameAndKeyValueAndAccess, \
            select_language_message, \
            GetAccess, \
            defaul_keyboard_func\
            )

    # Добавление языка
    bd_item_add.AddBDItem3RegisterHandlers(dp, \
            bd_item.GetCheckForTextFunc(add_language_button_name), \
            FSMCreateLanguage,\
            FSMCreateLanguage.name,\
            FSMCreateLanguage.desc, \
            FSMCreateLanguage.photo,\
            AddBDItemFunc, \
            SimpleMessageTemplateLegacy(language_create_name_message), \
            SimpleMessageTemplateLegacy(language_create_desc_message), \
            SimpleMessageTemplateLegacy(language_create_photo_message), \
            SimpleMessageTemplateLegacy(language_success_create_message), \
            None,\
            None, \
            None, \
            name_field, \
            desc_field, \
            photo_field, \
            GetButtonNameAndKeyValueAndAccess, \
            GetAccess, \
            GetStartLanguageKeyboardButtons\
            )

    # Редактирование языка
    edit_keyboard_func = GetEditLanguageKeyboardButtons

    def RegisterEdit(a_ButtonName, a_FSM, a_EditLanguage, a_FieldName, a_FieldType, a_AccessMode = user_access.AccessMode.EDIT):
        bd_item_edit.EditBDItemRegisterHandlers(dp, \
                None, \
                a_FSM, \
                bd_item.GetCheckForTextFunc(a_ButtonName), \
                language_select_to_edit_message, \
                ShowMessageTemplate(a_EditLanguage), \
                ShowMessageTemplate(language_success_edit_message), \
                table_name, \
                key_name, \
                None, \
                a_FieldName, \
                GetButtonNameAndKeyValueAndAccess, \
                GetAccess, \
                edit_keyboard_func, \
                access_mode = a_AccessMode, \
                field_type = a_FieldType\
                )

    dp.register_message_handler(simple_message.InfoMessageTemplateLegacy(language_start_edit_message, edit_keyboard_func, GetAccess, access_mode = user_access.AccessMode.EDIT), text = edit_language_button_name)
    RegisterEdit(edit_language_photo_button_name, FSMEditLanguagePhotoItem, language_edit_photo_message, photo_field, bd_item.FieldType.photo)
    RegisterEdit(edit_language_name_button_name, FSMEditLanguageNameItem, language_edit_name_message, name_field, bd_item.FieldType.text)
    RegisterEdit(edit_language_desc_button_name, FSMEditLanguageDeskItem, language_edit_desc_message, desc_field, bd_item.FieldType.text)
    RegisterEdit(edit_language_access_button_name, FSMEditLanguageAccessItem, language_edit_access_message, access_field, bd_item.FieldType.text)
'''
