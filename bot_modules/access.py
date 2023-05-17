# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Права пользователей

from bot_sys import keyboard, user_access, bot_bd, bd_table
from bot_modules import mod_simple_message, access_utils, mod_table_operate
from template import simple_message, sql_request, bd_item

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMRequestToBDAccess(StatesGroup):
    sqlRequest = State()


class FSMEditAccessItem(StatesGroup):
    item_field = State()


class FSMEditDefaultAccessItem(StatesGroup):
    item_field = State()
# ---------------------------------------------------------
# БД
module_name = 'access'

table_name = access_utils.table_name
mod_name_field = access_utils.mod_name_field
moduleaccess_field = access_utils.moduleaccess_field
mod_default_access_field = access_utils.mod_default_access_field

table = bd_table.Table(table_name, [
        bd_table.TableField(mod_name_field, bd_table.TableFieldDestiny.KEY, bd_table.TableFieldType.STR),
        bd_table.TableField(moduleaccess_field, bd_table.TableFieldDestiny.ACCESS, bd_table.TableFieldType.STR),
        bd_table.TableField(mod_default_access_field, bd_table.TableFieldDestiny.DEFAULT_ACCESS, bd_table.TableFieldType.STR),
        ])
# ---------------------------------------------------------
# Сообщения

start_message = '''
<b> Права пользователей находятся в стадии разработки</b>

Пока можете воспользоваться хардкорным способом через запросы к БД
'''

request_start_message = '''
**Задайте запрос к БД**

Можете воспользоваться следующими шаблонами:
1. `SELECT * FROM users` - Все пользователи
2. `SELECT * FROM module_access` - Все права к модулям
3. `UPDATE module_access SET modAccess = 'NEWACCESS' WHERE modName = 'MODNAME'` - Задать новые права NEWACCESS для модуля MODNAME
'''

help_message = '''
📄 Существует одна БД для работы с правами для модулей
Имя БД: module_access 
Поля:(modName, modAccess)

modAccess - строка
''' + user_access.user_access_readme

start_button_name = "⛀ Доступ пользователей"
sql_request_button_name = "⛁ Запрос к БД для редактирования доступа"
help_button_name = "📄 Информация по редактированию доступа"

# Редактирование доступа.

moduleaccess_select_to_edit_message = '''
Выберите модуль, который вы хотите отредактировать.
'''

edit_moduleaccess_access_button_name = "◇ Изменить доступ к модулю"
moduleaccess_edit_access_message = f'''
Текущий доступ к модулю #{mod_name_field}:
#{moduleaccess_field}

{user_access.user_access_readme}

Введите новую строку доступа:
'''

edit_moduleaccess_default_access_button_name = "◈ Изменить доступ по умолчанию к модулю "
moduleaccess_edit_default_access_message = f'''
Текущий доступ по умолчанию к модулю #{mod_name_field}:
#{mod_default_access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
'''
moduleaccess_success_edit_message = '''✅ Доступ к модулю успешно отредактирован!'''

button_names = {
    mod_simple_message.ButtonNames.START: start_button_name,
    mod_table_operate.ButtonNames.EDIT_ACCESS: "◇ Изменить доступ к модулю",
    mod_table_operate.ButtonNames.EDIT_DEFAULT_ACCESS: "◈ Изменить доступ по умолчанию к модулю ",
    }

messages = {
    mod_simple_message.Messages.START: start_message,
    mod_table_operate.Messages.EDIT_ACCESS: moduleaccess_edit_access_message,
    mod_table_operate.Messages.EDIT_DEFAULT_ACCESS: moduleaccess_edit_default_access_message,
    mod_table_operate.Messages.SUCCESS_EDIT: moduleaccess_success_edit_message,
}

fsm = {
    mod_table_operate.FSMs.EDIT_ACCESS: FSMEditAccessItem,
    mod_table_operate.FSMs.EDIT_DEFAULT_ACCESS: FSMEditDefaultAccessItem,
    }

init_access = f'{user_access.user_access_group_new}=-'

class ModuleAccess(mod_table_operate.TableOperateModule):
    def __init__(self, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(table, messages, button_names, fsm, None, None, init_access, a_ChildModuleNameList, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)
        self.m_SqlRequestButtonName = self.CreateButton('sql request', sql_request_button_name)
        self.m_RequestStartMessage = self.CreateMessage('equest start', request_start_message)

        self.m_HelpButtonName = self.CreateButton('help', help_button_name)
        self.m_HelpMessage = self.CreateMessage('help', help_message)

        self.m_HelpMessageHandler = simple_message.InfoMessageTemplate(
                self.m_Bot,
                self.m_HelpMessage,
                self.m_GetStartKeyboardButtonsFunc,
                None,
                self.m_GetAccessFunc
                )
    '''
    def GetInitBDCommands(self):
        return [
            f"""CREATE TABLE IF NOT EXISTS {table_name}(
                {mod_name_field} TEXT,
                {moduleaccess_field} TEXT,
                {mod_default_access_field} TEXT,
                UNIQUE({mod_name_field})
                );""",
            ] + super().GetInitBDCommands()
    '''
    def GetName(self):
        return module_name

    def GetStartKeyboardButtons(self, a_Message, a_UserGroups):
        mod_buttons = super().GetStartKeyboardButtons(a_Message, a_UserGroups)
        cur_buttons = [
                keyboard.ButtonWithAccess(self.m_SqlRequestButtonName, user_access.AccessMode.EDIT, self.GetAccess()), 
                keyboard.ButtonWithAccess(self.m_HelpButtonName , user_access.AccessMode.VIEW, self.GetAccess())
                ]
        return mod_buttons + keyboard.MakeButtons(cur_buttons, a_UserGroups)

    def RegisterHandlers(self):
        super().RegisterHandlers()
        sql_request.RequestToBDRegisterHandlers(
                self.m_Bot,
                self.m_SqlRequestButtonName,
                self.m_RequestStartMessage,
                FSMRequestToBDAccess,
                self.m_GetStartKeyboardButtonsFunc,
                user_access.AccessMode.EDIT,
                self.m_GetAccessFunc
                )
        self.m_Bot.RegisterMessageHandler(
                self.m_HelpMessageHandler, 
                bd_item.GetCheckForTextFunc(self.m_HelpButtonName)
                )


# ---------------------------------------------------------
# Работа с кнопками
'''
def GetEditAccessKeyboardButtons(a_Message, a_UserGroups):
    cur_buttons = [
        keyboard.ButtonWithAccess(sql_request_button_name, user_access.AccessMode.ACCEES_EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_moduleaccess_access_button_name, user_access.AccessMode.ACCEES_EDIT, GetAccess()),
        keyboard.ButtonWithAccess(edit_moduleaccess_default_access_button_name, user_access.AccessMode.ACCEES_EDIT, GetAccess()),
        keyboard.ButtonWithAccess(help_button_name, user_access.AccessMode.VIEW, GetAccess())
    ]
    mods = [start]
    return keyboard.MakeKeyboard(keyboard.GetButtons(mods) + cur_buttons, a_UserGroups)

# ---------------------------------------------------------
# Обработка сообщений

def GetButtonNameAndKeyValueAndAccess(a_Item):
    # ButtonName KeyValue Access
    return a_Item[0], a_Item[0], a_Item[1]

def ShowMessageTemplate(a_StringMessage):
    async def ShowMessage(a_CallbackQuery : types.CallbackQuery, a_Item):
        if (len(a_Item) < 3):
            return simple_message.WorkFuncResult(error_find_proj_message)

        msg = a_StringMessage.\
                replace(f'#{mod_name_field}', a_Item[0]).\
                replace(f'#{moduleaccess_field}', a_Item[1]).\
                replace(f'#{mod_default_access_field}', a_Item[2])
        return simple_message.WorkFuncResult(msg, item_access = a_Item[1])
    return ShowMessage

def SimpleMessageTemplateLegacy(a_StringMessage):
    async def ShowMessage(a_CallbackQuery : types.CallbackQuery):
        return simple_message.WorkFuncResult(a_StringMessage)
    return ShowMessage

# ---------------------------------------------------------
# Работа с базой данных 

def GetModuleAccessList():
    return bot_bd.SelectBDTemplate(table_name)()

# ---------------------------------------------------------
# API

def GetAccessForModule(a_ModuleName):
    alist = GetModuleAccessList()
    for i in alist:
        if i[0] == a_ModuleName:
            return i[1]
    return ''

def GetItemDefaultAccessForModule(a_ModuleName):
    alist = GetModuleAccessList()
    for i in alist:
        if i[0] == a_ModuleName:
            return i[2]
    return ''

# Инициализация БД
def GetInitBDCommands():
    return init_bd_cmds

def GetAccess():
    return GetAccessForModule(module_name)

# Доступные кнопки
def GetModuleButtons():
    return [keyboard.ButtonWithAccess(access_button_name, user_access.AccessMode.VIEW, GetAccess())]

# Обработка кнопок
def RegisterHandlers(dp : Dispatcher):
    defaul_keyboard_func = GetEditAccessKeyboardButtons
    dp.register_message_handler(simple_message.InfoMessageTemplateLegacy(access_start_message, defaul_keyboard_func, GetAccess), text = access_button_name)
    dp.register_message_handler(simple_message.InfoMessageTemplateLegacy(help_message, defaul_keyboard_func, GetAccess), text = help_button_name)

    sql_request.RequestToBDRegisterHandlers(dp, sql_request_button_name, request_start_message, FSMRequestToBDAccess, defaul_keyboard_func, user_access.AccessMode.ACCEES_EDIT, GetAccess)

    edit_keyboard_func = defaul_keyboard_func
    def RegisterEdit(a_ButtonName, a_FSM, a_EditMessage, a_FieldName, a_FieldType, a_AccessMode = user_access.AccessMode.ACCEES_EDIT):
        bd_item_edit.EditBDItemRegisterHandlers(dp, \
                None, \
                a_FSM, \
                bd_item.GetCheckForTextFunc(a_ButtonName), \
                moduleaccess_select_to_edit_message, \
                ShowMessageTemplate(a_EditMessage), \
                ShowMessageTemplate(moduleaccess_success_edit_message), \
                table_name, \
                mod_name_field, \
                None, \
                a_FieldName, \
                GetButtonNameAndKeyValueAndAccess, \
                GetAccess, \
                edit_keyboard_func, \
                access_mode = a_AccessMode, \
                field_type = a_FieldType\
                )
    RegisterEdit(edit_moduleaccess_access_button_name, FSMEditAccessItem, moduleaccess_edit_access_message, moduleaccess_field, bd_item.FieldType.text, user_access.AccessMode.ACCEES_EDIT)
    RegisterEdit(edit_moduleaccess_default_access_button_name, FSMEditDefaultAccessItem, moduleaccess_edit_default_access_message, mod_default_access_field, bd_item.FieldType.text, user_access.AccessMode.EDIT)

'''

