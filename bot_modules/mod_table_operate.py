# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Модуль для редактирования и просмотра таблицы в БД

from bot_sys import keyboard, user_access
from bot_modules import access_utils, mod_interface
from template import simple_message, bd_item

from enum import Enum
from enum import auto

class ButtonNames(Enum):
    START = auto() 
    LIST = auto() 
    ADD = auto() 
    EDIT = auto() 
    EDIT_PHOTO = auto() 
    EDIT_NAME = auto() 
    EDIT_DESC = auto() 
    EDIT_ACCESS = auto() 
    DEL = auto() 

class Messages(Enum):
    START = auto() 
    SELECT = auto() 
    ERROR_FIND = auto() 
    OPEN = auto() 
    CREATE_NAME = auto() 
    CREATE_DESC = auto() 
    CREATE_PHOTO = auto() 
    SUCCESS_CREATE = auto() 
    START_EDIT = auto() 
    SELECT_TO_EDIT = auto() 
    EDIT_PHOTO = auto() 
    EDIT_NAME = auto() 
    EDIT_DESC = auto() 
    EDIT_ACCESS = auto() 
    SUCCESS_EDIT = auto() 
    SELECT_TO_DELETE = auto() 
    SUCCESS_DELETE = auto() 

class FSMs:
    def __init__(self, a_FSMCreate, a_FSMEditName, a_FSMEditDesc, a_FSMEditPhoto, a_FSMEditAccess):
        self.m_FSMCreate = a_FSMCreate
        self.m_FSMEditName = a_FSMEditName
        self.m_FSMEditDesc = a_FSMEditDesc
        self.m_FSMEditPhoto = a_FSMEditPhoto
        self.m_FSMEditAccess = a_FSMEditAccess

# Предназначение поля в таблице
class TableFieldDestiny(Enum):
    KEY = auto()

class TableOperateModule(mod_simple_message.SimpleMessageModule):
    def __init__(self, a_Table, a_Messages, a_Buttons, a_FSMs, a_ParentModName, a_ChildModName, a_InitAccess, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(a_Messages[0], a_Buttons[0], a_InitAccess, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)
        self.m_Table = a_Table
        self.m_FSMs = a_FSMs
        self.m_EditModuleNameList = a_EditModuleNameList
        self.m_ChildModName = a_ChildModName
        self.m_ParentModName = a_ParentModName
        self.m_SelectPrefix = ''

        self.m_Buttons = {}
        for name, button_name in a_Buttons.items():
            self.m_Buttons[name] = self.CreateButton(name, button_name)

        self.m_Messages = {}
        for name, message in a_Messages.items():
            self.m_Messages[name] = self.CreateMessage(name, message)

        def GetEditKeyboardButtons(a_Message, a_UserGroups):
            return self.GetEditKeyboardButtons(a_Message, a_UserGroups)
        self.m_GetEditKeyboardButtonsFunc = GetEditKeyboardButtons

        def GetButtonNameAndKeyValueAndAccess(a_Item):
            return self.GetButtonNameAndKeyValueAndAccess(a_Item)
        self.m_GetButtonNameAndKeyValueAndAccessFunc = GetButtonNameAndKeyValueAndAccess

        async def PreDelete(a_CallbackQuery : types.CallbackQuery, a_Item):
            return self.PreDelete(a_Item)
        self.m_PreDeleteFunc = PreDelete

        async def PostDelete(a_CallbackQuery : types.CallbackQuery, a_ItemID):
            return self.PostDelete(a_Item)
        self.m_PostDeleteFunc = PostDelete

        def AddBDItemFunc(a_ItemData, a_UserID):
            return self.AddBDItemFunc(a_Item)
        self.m_AddBDItemFunc = AddBDItemFunc
 

    def GetButton(self, a_ButtonName):
        return self.m_Buttons.get(a_ButtonName, None)

    def GetMessage(self, a_MessageNames):
        return self.m_Messages.get(a_MessageNames, None)

    def GetInitBDCommands(self):
        return super(). GetInitBDCommands() + [
            self.m_Table.GetInitTableRequest(),
            ]

    def GetStartKeyboardButtons(self, a_Message, a_UserGroups):
        mod_buttons = super().GetStartKeyboardButtons(a_Message, a_UserGroups)
        cur_buttons = [
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.LIST), user_access.AccessMode.VIEW, GetAccess()),
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.ADD), user_access.AccessMode.ADD, GetAccess()),
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.DEL), user_access.AccessMode.DELETE, GetAccess()),
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.EDIT), user_access.AccessMode.EDIT, GetAccess())
                ]
        return mod_buttons + keyboard.MakeButtons(cur_buttons, a_UserGroups)

    def GetEditKeyboardButtons(self, a_Message, a_UserGroups):
        mod_buttons = self.GetButtons(self.m_EditModuleNameList)
        cur_buttons = [
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.EDIT_PHOTO), user_access.AccessMode.VIEW, GetAccess()),
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.EDIT_NAME), user_access.AccessMode.ADD, GetAccess()),
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.EDIT_DESC), user_access.AccessMode.DELETE, GetAccess()),
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.EDIT_ACCESS), user_access.AccessMode.EDIT, GetAccess())
                ]
        return mod_buttons + keyboard.MakeButtons(cur_buttons, a_UserGroups)

    def GetViewItemInlineKeyboardTemplate(self, a_ItemID):
        def GetViewItemInlineKeyboard(a_Message, a_UserGroups):
            return self.GetViewItemInlineKeyboard(a_Message, a_UserGroups, a_ItemID)
        return GetViewItemInlineKeyboard

    def GetSelectPrefix(self):
        return self.m_SelectPrefix

    def GetViewItemInlineKeyboard(self, a_Message, a_UserGroups, a_ItemID):
        if not self.m_ChildModName:
            return None
        child_mod = self.GetModule(self.m_ChildModName)
        cur_buttons = [
                keyboard.InlineButton(child_mod.GetButton(ButtonNames.LIST), child_mod.GetSelectPrefix(), a_ItemID, GetAccess(), user_access.AccessMode.VIEW),
                ]
        return keyboard.MakeInlineKeyboardButtons(cur_buttons, a_UserGroups)

    def GetButtonNameAndKeyValueAndAccess(self, a_Item):
        return \
                a_Item[self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.NAME)],
                a_Item[self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.KEY)],
                a_Item[self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.ACCESS)]

    def ShowMessageTemplate(self, a_MessageName : Message, keyboard_template_func = None):
        async def ShowMessage(a_CallbackQuery : types.CallbackQuery, a_Item):
            if len(a_Item) < self.m_Table.GetFieldsCount():
                return simple_message.WorkFuncResult(self.GetMessage(Messages.ERROR_FIND))

            msg = self.GetMessage(a_MessageName).StaticCopy()
            msg.UpdateDesc(table.ReplaceAllFieldTags(msg.GetDesc(), a_Item))
            msg.UpdatePhotoID(a_Item[self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.PHOTO)])

            keyboard_func = None
            if keyboard_template_func:
                keyboard_func = keyboard_template_func(a_Item[self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.KEY)])
            return simple_message.WorkFuncResult(msg, item_access = a_Item[self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.ACCESS)], keyboard_func = keyboard_func)
        return ShowMessage

    # TODO: delete?
    def SimpleMessageTemplate(self, a_MessageName : Message):
        async def ShowMessage(a_CallbackQuery, a_Item):
            return simple_message.WorkFuncResult(self.GetMessage(a_MessageName))
        return ShowMessage

    async def PreDelete(self, a_CallbackQuery, a_Item):
        if len(a_Item) < self.m_Table.GetFieldsCount():
            return simple_message.WorkFuncResult(error_find_proj_message)
        access = a_Item[self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.ACCESS)]
        return simple_message.WorkFuncResult(self.GetMessage(Messages.SUCCESS_DELETE), None, item_access = access)

    async def TaskPostDelete(self, a_CallbackQuery, a_ItemID):
        self.m_Log.Success(f'Задача №{a_ItemID} была удалена пользователем {a_CallbackQuery.from_user.id}.')
        #TODO: удалить вложенные 
        return simple_message.WorkFuncResult(self.GetMessage(Messages.SUCCESS_DELETE))

    def AddBDItemFunc(self, a_ItemData, a_UserID):
        table_name = self.m_Table.GetName()
        name_field = self.m_Table.GetFieldByDestiny(bd_table.TableFieldDestiny.NAME)
        photo_field = self.m_Table.GetFieldByDestiny(bd_table.TableFieldDestiny.PHOTO)
        desc_field = self.m_Table.GetFieldByDestiny(bd_table.TableFieldDestiny.DESC)
        access_field = self.m_Table.GetFieldByDestiny(bd_table.TableFieldDestiny.ACCESS)
        create_datetime_field = self.m_Table.GetFieldByDestiny(bd_table.TableFieldDestiny.CREATE_DATE)
        parent_id_field = self.m_Table.GetFieldByDestiny(bd_table.TableFieldDestiny.PARENT_ID)

        def_access = access_utils.GetItemDefaultAccessForModule(self.m_Bot, self.GetName())
        res, error = self.m_Bot.SQLRequest(f'INSERT INTO {table_name}({photo_field}, {name_field}, {desc_field}, {access_field}, {parent_id_field}, {create_datetime_field}) VALUES(?, ?, ?, ?, ?, {bot_bd.GetBDDateTimeNow()})', 
                commit = True, return_error = True, param = (a_ItemData[photo_field], a_ItemData[name_field], a_ItemData[desc_field], def_access + f";{a_UserID}=+", a_ItemData[parent_id_field]))

        if error:
            self.m_Log.Error(f'Пользоватлель {a_UserID}. Ошибка добавления записи в таблицу {table_name} ({a_ItemData[photo_field]}, {a_ItemData[name_field]}, {a_ItemData[desc_field]}, {def_access}).')
        else:
            self.m_Log.Success(f'Пользоватлель {a_UserID}. Добавлена запись в таблицу {table_name} ({a_ItemData[photo_field]}, {a_ItemData[name_field]}, {a_ItemData[desc_field]}, {def_access}).')

        return res, error

    def RegisterSelect(self, a_ButtonName, access_mode):
        if self.m_ParentModName:
            parent_mod = self.GetModule(self.m_ParentModName)
            a_Prefix = parent_mod.RegisterSelect(a_ButtonName, access_mode)
            a_Prefix =  bd_item_select.NextSelectBDItemRegisterHandlers(self.m_Bot, \
                a_Prefix, \
                self.m_Table.GetFieldByDestiny(bd_table.TableFieldDestiny.PARENT_ID), \
                self.m_Table.GetName(), \
                self.m_Table.GetFieldByDestiny(bd_table.TableFieldDestiny.KEY), \
                self.m_GetButtonNameAndKeyValueAndAccessFunc, \
                self.GetMessage(Messages.SELECT), \
                self.m_GetAccessFunc,\
                access_mode = access_mode\
                )
        else:
            a_PrefixBase = a_ButtonName.GetDesc()
            a_Prefix =   bd_item_select.FirstSelectBDItemRegisterHandlers(self.m_Bot, \
                a_PrefixBase, \
                a_ButtonName, \
                self.m_Table.GetName(), \
                self.m_Table.GetFieldByDestiny(bd_table.TableFieldDestiny.KEY), \
                self.m_GetButtonNameAndKeyValueAndAccessFunc, \
                self.GetMessage(Messages.SELECT), \
                self.m_GetAccessFunc,\
                access_mode = access_mode\
                )
        return a_Prefix

    def RegisterHandlers(self):
        super().RegisterHandlers()
        table_name = self.m_Table.GetName()
        key_name = self.m_Table.GetFieldByDestiny(bd_table.TableFieldDestiny.KEY)
        name_field = self.m_Table.GetFieldByDestiny(bd_table.TableFieldDestiny.NAME)
        desc_field = self.m_Table.GetFieldByDestiny(bd_table.TableFieldDestiny.DESC)
        photo_field = self.m_Table.GetFieldByDestiny(bd_table.TableFieldDestiny.PHOTO)
        access_field = self.m_Table.GetFieldByDestiny(bd_table.TableFieldDestiny.ACCESS)
        parent_id_field = self.m_Table.GetFieldByDestiny(bd_table.TableFieldDestiny.PARENT_ID)

        parent_table_name = None
        parent_key_name = None
        if self.m_ParentModName:
            parent_mod = self.GetModule(self.m_ParentModName)
            parent_table_name = parent_mod.m_Table.GetName()
            parent_key_name = parent_mod.m_Table.GetFieldByDestiny(bd_table.TableFieldDestiny.KEY)

        def GetViewItemInlineKeyboardTemplate(a_ItemID):
            def GetViewItemInlineKeyboard(a_ItemID):
                return self.GetViewItemInlineKeyboardTemplate(a_ItemID)
            return GetViewItemInlineKeyboard

        GetButtonNameAndKeyValueAndAccess = self.m_GetButtonNameAndKeyValueAndAccessFunc
        GetAccess = self.m_GetAccessFunc

        defaul_keyboard_func = self.m_GetStartTaskKeyboardButtonsFunc

        sql_request.RequestToBDRegisterHandlers(
                self.m_Bot,
                self.m_SqlRequestButtonName,
                self.m_RequestStartMessage,
                FSMRequestToBDAccess,
                self.m_GetStartKeyboardButtonsFunc,
                user_access.AccessMode.EDIT,
                self.m_GetAccessFunc
                )

        # Список 
        a_ButtonName = self.GetButton(ButtonNames.LIST)
        if a_ButtonName:
            a_Prefix = self.RegisterSelect(a_ButtonName, user_access.AccessMode.VIEW)
            bd_item_view.LastSelectAndShowBDItemRegisterHandlers(self.m_Bot, \
                    a_Prefix,\
                    parent_id_field, \
                    table_name,\
                    key_name, \
                    self.ShowMessageTemplate(self.GetMessage(Messages.OPEN), GetViewItemInlineKeyboardTemplate), \
                    GetButtonNameAndKeyValueAndAccess, \
                    self.GetMessage(Messages.SELECT), \
                    GetAccess, \
                    defaul_keyboard_func, \
                    access_mode = user_access.AccessMode.VIEW\
                    )
        self.m_SelectPrefix = a_Prefix

        # Удаление 
        a_ButtonName = self.GetButton(ButtonNames.DEL)
        if a_ButtonName:
            a_Prefix = self.RegisterSelect(a_ButtonName, user_access.AccessMode.DELETE)
            bd_item_delete.DeleteBDItemRegisterHandlers(self.m_Bot, \
                    a_Prefix, \
                    bd_item.GetCheckForPrefixFunc(a_Prefix), \
                    table_name, \
                    key_name, \
                    parent_id_field, \
                    self.m_PreDeleteFunc, \
                    self.m_PostDeleteFunc, \
                    GetButtonNameAndKeyValueAndAccess, \
                    self.GetMessage(Messages.SELECT), \
                    GetAccess, \
                    defaul_keyboard_func\
                    )

        # Добавление 
        a_ButtonName = self.GetButton(ButtonNames.ADD)
        if a_ButtonName:
            a_Prefix = self.RegisterSelect(a_ButtonName, user_access.AccessMode.ADD)
                    bd_item_add.AddBDItem3RegisterHandlers(self.m_Bot, \
                    bd_item.GetCheckForPrefixFunc(a_Prefix), \
                    self.m_FSMs.m_FSMCreate, \
                    self.m_FSMs.m_FSMCreate.name,\
                    self.m_FSMs.m_FSMCreate.desc, \
                    self.m_FSMs.m_FSMCreate.photo,\
                    self.m_AddBDItemFunc, \
                    self.ShowMessageTemplate(self.GetMessage(Messages.CREATE_NAME)), \
                    self.ShowMessageTemplate(self.GetMessage(Messages.CREATE_DESC)), \
                    self.ShowMessageTemplate(self.GetMessage(Messages.CREATE_PHOTO)), \
                    self.ShowMessageTemplate(self.GetMessage(Messages.SUCCESS_CREATE)), \
                    a_Prefix,\
                    parent_table_name, \
                    parent_key_name, \
                    name_field, \
                    desc_field, \
                    photo_field, \
                    GetButtonNameAndKeyValueAndAccess, \
                    GetAccess, \
                    self.m_GetStartTaskKeyboardButtonsFunc\
                    )

    # Редактирование
        edit_keyboard_func = self.m_GetEditTaskKeyboardButtonsFunc
        def RegisterEdit(a_ButtonName, a_FSM, a_EditMessage, a_FieldName, a_FieldType, a_AccessMode = user_access.AccessMode.EDIT):
            if not a_ButtonName:
                return
            a_Prefix = self.RegisterSelect(a_ButtonName, a_AccessMode)
            bd_item_edit.EditBDItemRegisterHandlers(self.m_Bot, \
                a_Prefix, \
                a_FSM, \
                bd_item.GetCheckForPrefixFunc(a_Prefix), \
                self.GetMessage(Messages.SELECT_TO_EDIT), \
                self.ShowMessageTemplate(a_EditMessage), \
                self.ShowMessageTemplate(self.GetMessage(Messages.SUCCESS_EDIT)), \
                table_name, \
                key_name, \
                parent_id_field, \
                a_FieldName, \
                GetButtonNameAndKeyValueAndAccess, \
                GetAccess, \
                edit_keyboard_func, \
                access_mode = a_AccessMode, \
                field_type = a_FieldType\
                )

        a_ButtonName = self.GetButton(ButtonNames.EDIT)
        if a_ButtonName:
            self.m_Bot.RegisterMessageHandler(\
                simple_message.InfoMessageTemplateLegacy(\
                        self.GetMessage(Messages.START_EDIT),\
                        edit_keyboard_func,\
                        GetAccess,\
                        access_mode = user_access.AccessMode.EDIT),\
                        bd_item.GetCheckForTextFunc(a_ButtonName)\
                        )

        RegisterEdit(self.GetButton(ButtonNames.EDIT_NAME), self.m_FSMs.m_FSMEditName, self.GetMessage(Messages.EDIT_NAME), name_field, bd_item.FieldType.text)
        RegisterEdit(self.GetButton(ButtonNames.EDIT_DESC), self.m_FSMs.m_FSMEditDesc, self.GetMessage(Messages.EDIT_DESC), desc_field, bd_item.FieldType.text)
        RegisterEdit(self.GetButton(ButtonNames.EDIT_PHOTO), self.m_FSMs.m_FSMEditPhoto, self.GetMessage(Messages.EDIT_PHOTO), photo_field, bd_item.FieldType.photo)
        RegisterEdit(self.GetButton(ButtonNames.EDIT_ACCESS), self.m_FSMs.m_FSMEditAccess, self.GetMessage(Messages.EDIT_ACCESS), access_field, bd_item.FieldType.text)
