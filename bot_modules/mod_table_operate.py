# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Модуль для редактирования и просмотра таблицы в БД

from bot_sys import keyboard, user_access, bd_table, bot_bd
from bot_modules import access_utils, mod_simple_message
from template import simple_message, bd_item, bd_item_select, bd_item_view, bd_item_delete, bd_item_add, bd_item_edit

from enum import Enum
from enum import auto

class ButtonNames(Enum):
    LIST = auto() 
    ADD = auto() 
    EDIT = auto() 
    EDIT_PHOTO = auto() 
    EDIT_NAME = auto() 
    EDIT_DESC = auto() 
    EDIT_ACCESS = auto() 
    EDIT_DEFAULT_ACCESS = auto() 
    DEL = auto() 

class Messages(Enum):
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
    EDIT_DEFAULT_ACCESS = auto() 
    SUCCESS_EDIT = auto() 
    SELECT_TO_DELETE = auto() 
    SUCCESS_DELETE = auto() 

class FSMs(Enum):
    CREATE = auto() 
    EDIT_PHOTO = auto() 
    EDIT_NAME = auto() 
    EDIT_DESC = auto() 
    EDIT_ACCESS = auto() 
    EDIT_DEFAULT_ACCESS = auto() 

class TableOperateModule(mod_simple_message.SimpleMessageModule):
    def __init__(self, a_Table, a_Messages, a_Buttons, a_FSMs, a_ParentModName, a_ChildModName, a_InitAccess, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(a_Messages, a_Buttons, a_InitAccess, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)
        self.m_Table = a_Table
        self.m_FSMs = a_FSMs
        self.m_EditModuleNameList = a_EditModuleNameList
        self.m_ChildModName = a_ChildModName
        self.m_ParentModName = a_ParentModName
        self.m_SelectPrefix = ''

        def GetEditKeyboardButtons(a_Message, a_UserGroups):
            return self.GetEditKeyboardButtons(a_Message, a_UserGroups)
        self.m_GetEditKeyboardButtonsFunc = GetEditKeyboardButtons

        def GetButtonNameAndKeyValueAndAccess(a_Item):
            return self.GetButtonNameAndKeyValueAndAccess(a_Item)
        self.m_GetButtonNameAndKeyValueAndAccessFunc = GetButtonNameAndKeyValueAndAccess

        async def PreDelete(a_CallbackQuery, a_Item):
            return await self.PreDelete(a_CallbackQuery, a_Item)
        self.m_PreDeleteFunc = PreDelete

        async def PostDelete(a_CallbackQuery, a_ItemID):
            return await self.PostDelete(a_CallbackQuery, a_ItemID)
        self.m_PostDeleteFunc = PostDelete

        def AddBDItemFunc(a_ItemData, a_UserID):
            return self.AddBDItemFunc(a_ItemData, a_UserID)
        self.m_AddBDItemFunc = AddBDItemFunc
 
    def GetFSM(self, a_FSMName):
        return self.m_FSMs.get(a_FSMName, None)

    def GetInitBDCommands(self):
        return super(). GetInitBDCommands() + [
            self.m_Table.GetInitTableRequest(),
            ]

    def GetStartKeyboardButtons(self, a_Message, a_UserGroups):
        mod_buttons = super().GetStartKeyboardButtons(a_Message, a_UserGroups)
        cur_buttons = [
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.LIST), user_access.AccessMode.VIEW, self.GetAccess()),
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.ADD), user_access.AccessMode.ADD, self.GetAccess()),
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.DEL), user_access.AccessMode.DELETE, self.GetAccess()),
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.EDIT), user_access.AccessMode.EDIT, self.GetAccess()),
                ]
        return mod_buttons + keyboard.MakeButtons(cur_buttons, a_UserGroups)

    def GetEditKeyboardButtons(self, a_Message, a_UserGroups):
        mod_buttons = keyboard.MakeButtons(self.GetButtons(self.m_EditModuleNameList), a_UserGroups)
        cur_buttons = [
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.EDIT_PHOTO), user_access.AccessMode.VIEW, self.GetAccess()),
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.EDIT_NAME), user_access.AccessMode.ADD, self.GetAccess()),
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.EDIT_DESC), user_access.AccessMode.DELETE, self.GetAccess()),
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.EDIT_ACCESS), user_access.AccessMode.DELETE, self.GetAccess()),
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.EDIT_DEFAULT_ACCESS), user_access.AccessMode.EDIT, self.GetAccess()),
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
                keyboard.InlineButtonWithAccess(child_mod.GetButton(ButtonNames.LIST), child_mod.GetSelectPrefix(), a_ItemID, self.GetAccess(), user_access.AccessMode.VIEW),
                ]
        return keyboard.MakeInlineKeyboardButtons(cur_buttons, a_UserGroups)

    def GetButtonNameAndKeyValueAndAccess(self, a_Item):
        return \
                a_Item[self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.NAME)],\
                a_Item[self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.KEY)],\
                a_Item[self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.ACCESS)]

    def ShowMessageTemplate(self, a_Message, Inline_keyboard_template_func = None):
        async def ShowMessage(a_CallbackQuery, a_Item):
            msg = a_Message.StaticCopy()
            # TODO: добавить поддержку языка в a_MessageName
            Inline_keyboard_func = None
            item_access = None
            if a_Item:
                if len(a_Item) < self.m_Table.GetFieldsCount() - 1: # Для проектов это нужно. Там на 1 меньше поле. TODO разделить отправку сообщений item_access и Inline_keyboard_func
                    return simple_message.WorkFuncResult(self.GetMessage(Messages.ERROR_FIND))
                elif len(a_Item) == self.m_Table.GetFieldsCount():
                    msg.UpdateDesc(self.m_Table.ReplaceAllFieldTags(msg.GetDesc(), a_Item))
                    photo_field = self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.PHOTO)
                    if photo_field:
                        msg.UpdatePhotoID(a_Item[photo_field])
                item_access = a_Item[self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.ACCESS)]
                if Inline_keyboard_template_func:
                    Inline_keyboard_func = Inline_keyboard_template_func(a_Item[self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.KEY)])

            return simple_message.WorkFuncResult(msg, item_access = item_access, Inline_keyboard_func = Inline_keyboard_func)
        return ShowMessage

    # TODO: delete?
    def SimpleMessageTemplate(self, a_MessageName : Messages):
        async def ShowMessage(a_CallbackQuery, a_Item):
            return simple_message.WorkFuncResult(self.GetMessage(a_MessageName))
        return ShowMessage

    async def PreDelete(self, a_CallbackQuery, a_Item):
        if len(a_Item) < self.m_Table.GetFieldsCount():
            return simple_message.WorkFuncResult(error_find_proj_message)
        access = a_Item[self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.ACCESS)]
        return simple_message.WorkFuncResult(self.GetMessage(Messages.SUCCESS_DELETE), None, item_access = access)

    async def PostDelete(self, a_CallbackQuery, a_ItemID):
        self.m_Log.Success(f'Задача №{a_ItemID} была удалена пользователем {a_CallbackQuery.from_user.id}.')
        #TODO: удалить вложенные 
        self.OnChange()
        return simple_message.WorkFuncResult(self.GetMessage(Messages.SUCCESS_DELETE))

    def AddBDItemFunc(self, a_ItemData, a_UserID):
        table_name = self.m_Table.GetName()
        name_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.NAME)
        photo_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PHOTO)
        desc_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.DESC)
        access_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.ACCESS)
        create_datetime_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.CREATE_DATE)
        parent_id_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PARENT_ID)

        res, error = None, None
        def_access = access_utils.GetItemDefaultAccessForModule(self.m_Bot, self.GetName())
        #TODO сделать список полей, чтобы запрос генерировался автоматически.
        if parent_id_field:
            res, error = self.m_Bot.SQLRequest(f'INSERT INTO {table_name}({photo_field}, {name_field}, {desc_field}, {access_field}, {parent_id_field}, {create_datetime_field}) VALUES(?, ?, ?, ?, ?, {bot_bd.GetBDDateTimeNow()})', 
                    commit = True, return_error = True, param = (a_ItemData[photo_field], a_ItemData[name_field], a_ItemData[desc_field], def_access + f";{a_UserID}=+", a_ItemData[parent_id_field]))
        else:
            res, error = self.m_Bot.SQLRequest(f'INSERT INTO {table_name}({photo_field}, {name_field}, {desc_field}, {access_field}, {create_datetime_field}) VALUES(?, ?, ?, ?, {bot_bd.GetBDDateTimeNow()})', 
                    commit = True, return_error = True, param = (a_ItemData[photo_field], a_ItemData[name_field], a_ItemData[desc_field], def_access + f";{a_UserID}=+"))

        self.OnChange()
        if error:
            self.m_Log.Error(f'Пользоватлель {a_UserID}. Ошибка добавления записи в таблицу {table_name} ({a_ItemData[photo_field]}, {a_ItemData[name_field]}, {a_ItemData[desc_field]}, {def_access}).')
        else:
            self.m_Log.Success(f'Пользоватлель {a_UserID}. Добавлена запись в таблицу {table_name} ({a_ItemData[photo_field]}, {a_ItemData[name_field]}, {a_ItemData[desc_field]}, {def_access}).')

        return res, error

    def RegisterSelect(self, a_ButtonName, access_mode, only_parent = False):
        a_Prefix = None
        if self.m_ParentModName:
            parent_mod = self.GetModule(self.m_ParentModName)
            a_Prefix = parent_mod.RegisterSelect(a_ButtonName, access_mode, only_parent = False)
            if not only_parent:
                a_Prefix =  bd_item_select.NextSelectBDItemRegisterHandlers(self.m_Bot, \
                        a_Prefix, \
                        self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PARENT_ID), \
                        self.m_Table.GetName(), \
                        self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.KEY), \
                        self.m_GetButtonNameAndKeyValueAndAccessFunc, \
                        self.GetMessage(Messages.SELECT), \
                        self.m_GetAccessFunc,\
                        access_mode = access_mode\
                        )
        else:
            if not only_parent:
                a_PrefixBase = a_ButtonName.GetDesc()
                a_Prefix =   bd_item_select.FirstSelectBDItemRegisterHandlers(self.m_Bot, \
                        a_PrefixBase, \
                        a_ButtonName, \
                        self.m_Table.GetName(), \
                        self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.KEY), \
                        self.m_GetButtonNameAndKeyValueAndAccessFunc, \
                        self.GetMessage(Messages.SELECT), \
                        self.m_GetAccessFunc,\
                        access_mode = access_mode\
                        )
        return a_Prefix

    def RegisterHandlers(self):
        super().RegisterHandlers()
        table_name = self.m_Table.GetName()
        key_name = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.KEY)
        name_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.NAME)
        desc_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.DESC)
        photo_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PHOTO)
        access_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.ACCESS)
        def_access_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.DEFAULT_ACCESS)
        parent_id_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PARENT_ID)

        parent_table_name = None
        parent_key_name = None
        if self.m_ParentModName:
            parent_mod = self.GetModule(self.m_ParentModName)
            parent_table_name = parent_mod.m_Table.GetName()
            parent_key_name = parent_mod.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.KEY)

        def GetViewItemInlineKeyboardTemplate(a_ItemID):
            return self.GetViewItemInlineKeyboardTemplate(a_ItemID)

        GetButtonNameAndKeyValueAndAccess = self.m_GetButtonNameAndKeyValueAndAccessFunc
        GetAccess = self.m_GetAccessFunc

        defaul_keyboard_func = self.m_GetStartKeyboardButtonsFunc

        # Список 
        a_ButtonName = self.GetButton(ButtonNames.LIST)
        if a_ButtonName:
            a_Prefix = self.RegisterSelect(a_ButtonName, user_access.AccessMode.VIEW, only_parent = True)
            if a_Prefix:
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
            else:
                bd_item_view.FirstSelectAndShowBDItemRegisterHandlers(self.m_Bot, \
                        a_ButtonName, \
                        table_name, \
                        key_name, \
                        self.ShowMessageTemplate(self.GetMessage(Messages.OPEN), GetViewItemInlineKeyboardTemplate), \
                        GetButtonNameAndKeyValueAndAccess, \
                        self.GetMessage(Messages.SELECT), \
                        GetAccess, \
                        defaul_keyboard_func\
                        )
            self.m_SelectPrefix = a_Prefix

        # Удаление 
        a_ButtonName = self.GetButton(ButtonNames.DEL)
        if a_ButtonName:
            a_Prefix = self.RegisterSelect(a_ButtonName, user_access.AccessMode.DELETE)
            bd_item_delete.DeleteBDItemRegisterHandlers(self.m_Bot, \
                    a_Prefix, \
                    table_name, \
                    key_name, \
                    self.m_PreDeleteFunc, \
                    self.m_PostDeleteFunc, \
                    GetAccess, \
                    defaul_keyboard_func\
                    )

        # Добавление 
        a_ButtonName = self.GetButton(ButtonNames.ADD)
        if a_ButtonName:
            a_Prefix = self.RegisterSelect(a_ButtonName, user_access.AccessMode.ADD, only_parent = True)

            check_func = bd_item.GetCheckForTextFunc(a_ButtonName)
            if a_Prefix:
                check_func = bd_item.GetCheckForPrefixFunc(a_Prefix)

            bd_item_add.AddBDItem3RegisterHandlers(self.m_Bot, \
                    check_func, \
                    self.GetFSM(FSMs.CREATE), \
                    self.GetFSM(FSMs.CREATE).name,\
                    self.GetFSM(FSMs.CREATE).desc, \
                    self.GetFSM(FSMs.CREATE).photo,\
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
                    self.m_GetStartKeyboardButtonsFunc\
                    )

        # Редактирование
        edit_keyboard_func = self.m_GetEditKeyboardButtonsFunc
        def RegisterEdit(a_ButtonName, a_FSM, a_EditMessage, a_FieldName, a_FieldType, a_AccessMode = user_access.AccessMode.EDIT):
            if not a_ButtonName:
                return

            def OnChange():
                return self.OnChange()

            a_Prefix = self.RegisterSelect(a_ButtonName, a_AccessMode, only_parent = True)
            check_func = bd_item.GetCheckForTextFunc(a_ButtonName)
            if a_Prefix:
                check_func = bd_item.GetCheckForPrefixFunc(a_Prefix)
            #print(a_ButtonName, a_Prefix, check_func)
            bd_item_edit.EditBDItemRegisterHandlers(self.m_Bot, \
                a_Prefix, \
                a_FSM, \
                check_func, \
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
                OnChange,\
                access_mode = a_AccessMode, \
                field_type = a_FieldType\
                )

        a_ButtonName = self.GetButton(ButtonNames.EDIT)
        if a_ButtonName:
            self.m_Bot.RegisterMessageHandler(\
                simple_message.InfoMessageTemplate(\
                        self.m_Bot,\
                        self.GetMessage(Messages.START_EDIT),\
                        edit_keyboard_func,\
                        None,\
                        GetAccess,\
                        access_mode = user_access.AccessMode.EDIT),\
                        bd_item.GetCheckForTextFunc(a_ButtonName)\
                        )

        RegisterEdit(self.GetButton(ButtonNames.EDIT_NAME), self.GetFSM(FSMs.EDIT_NAME), self.GetMessage(Messages.EDIT_NAME), name_field, bd_item.FieldType.text)
        RegisterEdit(self.GetButton(ButtonNames.EDIT_DESC), self.GetFSM(FSMs.EDIT_DESC), self.GetMessage(Messages.EDIT_DESC), desc_field, bd_item.FieldType.text)
        RegisterEdit(self.GetButton(ButtonNames.EDIT_PHOTO), self.GetFSM(FSMs.EDIT_PHOTO), self.GetMessage(Messages.EDIT_PHOTO), photo_field, bd_item.FieldType.photo)
        RegisterEdit(self.GetButton(ButtonNames.EDIT_ACCESS), self.GetFSM(FSMs.EDIT_ACCESS), self.GetMessage(Messages.EDIT_ACCESS), access_field, bd_item.FieldType.text)
        RegisterEdit(self.GetButton(ButtonNames.EDIT_DEFAULT_ACCESS), self.GetFSM(FSMs.EDIT_DEFAULT_ACCESS), self.GetMessage(Messages.EDIT_DEFAULT_ACCESS), def_access_field, bd_item.FieldType.text)

    def OnChange(self):
        pass
