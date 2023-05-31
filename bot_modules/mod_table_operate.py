# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Модуль для редактирования и просмотра таблицы в БД

from bot_sys import keyboard, user_access, bd_table, bot_bd
from bot_modules import access_utils, mod_simple_message
from template import simple_message, bd_item, bd_item_select, bd_item_view, bd_item_delete, bd_item_add, bd_item_edit

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from enum import Enum
from enum import auto

def EditButton(a_BDTableDestiny):
    return 'edit ' + str(a_BDTableDestiny)

def EnumButton(a_EnumItem):
    return 'enum ' + str(a_EnumItem)

def EditMessage(a_BDTableDestiny):
    return 'edit ' + str(a_BDTableDestiny)

def CreateMessage(a_BDTableDestiny):
    return 'create ' + str(a_BDTableDestiny)

def EnumMessageForView(a_EnumItem):
    return 'enum ' + str(a_EnumItem)

def NotificationMessage(a_EnumItem):
    return 'notification ' + str(a_EnumItem)

class ButtonNames(Enum):
    LIST = auto() 
    ADD = auto() 
    EDIT = auto() 
    DEL = auto() 

class Messages(Enum):
    SELECT = auto() 
    ERROR_FIND = auto() 
    OPEN = auto() 
    SUCCESS_CREATE = auto() 
    START_EDIT = auto() 
    SELECT_TO_EDIT = auto() 
    SUCCESS_EDIT = auto() 
    SELECT_TO_DELETE = auto() 
    SUCCESS_DELETE = auto() 

class FSMs(Enum):
    CREATE = auto() 

create_fsms_cmd = '''
class FSMCreate{a_ModName}(StatesGroup):
    name = State()
    desc = State()
    photo = State()


fsm = {
    FSMs.CREATE: FSMCreate{a_ModName},
}
'''

def MakeFSMs(a_ModName):
    cmd = create_fsms_cmd.replace("{a_ModName}", a_ModName)
    _locals = locals()
    exec(cmd, globals(), _locals)
    return _locals['fsm']


edit_fsm_cmd = '''
class FSMEdit{a_ModName}_{a_FieldName}_Item(StatesGroup):
    item_field = State()
    
fsm = FSMEdit{a_ModName}_{a_FieldName}_Item
'''

def MakeFSMForEdit(a_ModName, a_FieldName):
    cmd = edit_fsm_cmd.replace("{a_ModName}", a_ModName).replace("{a_FieldName}", a_FieldName)
    print ('cmd', cmd)
    _locals = locals()
    exec(cmd, globals(), _locals)
    return _locals['fsm']

class TableOperateModule(mod_simple_message.SimpleMessageModule):
    def __init__(self, a_Table, a_Messages, a_Buttons, a_ParentModName, a_ChildModName, a_InitAccess, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(a_Messages, a_Buttons, a_InitAccess, a_ChildModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)
        self.m_Table = a_Table
        self.m_FSMs = MakeFSMs(self.GetName()) 
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

        async def AddBDItemFunc(a_ItemData, a_UserID):
            return await self.AddBDItemFunc(a_ItemData, a_UserID)
        self.m_AddBDItemFunc = AddBDItemFunc
 
    def GetFSM(self, a_FSMName):
        return self.m_FSMs.get(a_FSMName, None)

    def GetInitBDCommands(self):
        return  [
            self.m_Table.GetInitTableRequest(),
            ] + super().GetInitBDCommands()

    def GetStartKeyboardButtons(self, a_Message, a_UserGroups):
        mod_buttons = super().GetStartKeyboardButtons(a_Message, a_UserGroups)
        cur_buttons = [
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.LIST), user_access.AccessMode.VIEW, self.GetAccess()),
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.ADD), user_access.AccessMode.ADD, self.GetAccess()),
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.DEL), user_access.AccessMode.DELETE, self.GetAccess()),
                keyboard.ButtonWithAccess(self.GetButton(ButtonNames.EDIT), user_access.AccessMode.EDIT, self.GetAccess()),
                ]
        return mod_buttons + keyboard.MakeButtons(self.m_Bot, cur_buttons, a_UserGroups)

    def GetEditKeyboardButtons(self, a_Message, a_UserGroups):
        mod_buttons = keyboard.MakeButtons(self.m_Bot, self.GetButtons(self.m_EditModuleNameList), a_UserGroups)
        cur_buttons = []
        for f in self.m_Table.GetFields():
            access = user_access.AccessMode.EDIT
            if f.m_Destiny == bd_table.TableFieldDestiny.ACCESS or f.m_Destiny == bd_table.TableFieldDestiny.DEFAULT_ACCESS:
                access = user_access.AccessMode.ACCEES_EDIT
            cur_buttons += [keyboard.ButtonWithAccess(self.GetButton(EditButton(f.m_Destiny)), access, self.GetAccess()),]
        return mod_buttons + keyboard.MakeButtons(self.m_Bot, cur_buttons, a_UserGroups)

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
        return keyboard.MakeInlineKeyboardButtons(self.m_Bot, cur_buttons, a_UserGroups)

    def GetButtonNameAndKeyValueAndAccess(self, a_Item):
        key_name_id = self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.KEY)
        name_field_id = self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.NAME)
        access_field_id = self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.ACCESS)
        assert key_name_id != None
        assert name_field_id != None
        assert access_field_id != None
        return \
                a_Item[name_field_id],\
                a_Item[key_name_id],\
                a_Item[access_field_id]

    def UpdateMessage(self, a_Msg, a_Lang, a_Item, a_EnablePhoto = False):
        a_Msg.UpdateDesc(self.m_Table.ReplaceAllFieldTags(a_Msg.GetDesc(), a_Item))
        photos = []
        field_id = 0
        for f in self.m_Table.GetFields():
            if f.m_Type == bd_table.TableFieldType.ENUM:
                for s in f.m_Enum:
                    msg = self.GetMessage(EnumMessageForView(s))
                    if msg:
                        a_Msg.UpdateDesc(a_Msg.GetDesc().replace(str(s), str(msg.GetMessageForLang(a_Lang).StaticCopy())))
            elif f.m_Type == bd_table.TableFieldType.PHOTO:
                photos += [str(a_Item[field_id])]
            field_id += 1
        if a_EnablePhoto:
            a_Msg.UpdatePhotoID(','.join(photos))
        return a_Msg

    def ShowMessageTemplate(self, a_Message, Inline_keyboard_template_func = None, a_EnablePhoto = False):
        async def ShowMessage(a_CallbackQuery, a_Item):
            msg = a_Message.StaticCopy()
            # TODO: добавить поддержку языка в a_MessageName
            Inline_keyboard_func = None
            item_access = None
            if a_Item:
                if len(a_Item) < self.m_Table.GetFieldsCount() - 1: # Для проектов это нужно. Там на 1 меньше поле. TODO разделить отправку сообщений item_access и Inline_keyboard_func
                    return simple_message.WorkFuncResult(self.GetMessage(Messages.ERROR_FIND))
                elif len(a_Item) == self.m_Table.GetFieldsCount():
                    lang = str(a_CallbackQuery.from_user.language_code)
                    msg = msg.GetMessageForLang(lang).StaticCopy()
                    msg = self.UpdateMessage(msg, lang, a_Item, a_EnablePhoto = a_EnablePhoto)
                item_access = a_Item[self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.ACCESS)]
                if Inline_keyboard_template_func:
                    Inline_keyboard_func = Inline_keyboard_template_func(a_Item[self.m_Table.GetFieldIDByDestiny(bd_table.TableFieldDestiny.KEY)])

            return simple_message.WorkFuncResult(msg, item_access = item_access, Inline_keyboard_func = Inline_keyboard_func)
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

    async def AddBDItemFunc(self, a_ItemData, a_UserID):
        table_name = self.m_Table.GetName()
        name_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.NAME)
        photo_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PHOTO)
        desc_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.DESC)
        access_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.ACCESS)
        create_datetime_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.CREATE_DATE)
        parent_id_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PARENT_ID)

        def_access = access_utils.GetItemDefaultAccessForModule(self.m_Bot, self.GetName())

        fields = []
        values = []
        param = ()
        for f in self.m_Table.GetFields():
            d = f.m_Destiny
            n = f.m_Name
            if d == bd_table.TableFieldDestiny.KEY:
                continue
            elif d == bd_table.TableFieldDestiny.CREATE_DATE:
                fields += [n]
                values += [bot_bd.GetBDDateTimeNow()]
            elif d == bd_table.TableFieldDestiny.ACCESS:
                fields += [n]
                values += ['?']
                param += (def_access + f";{a_UserID}=+", )
            else:
                fields += [n]
                values += ['?']
                param += (a_ItemData[n], )

        request = f'INSERT INTO {table_name}({",".join(fields)}) VALUES({",".join(values)})'
        print('request', request, param)
        res, error = self.m_Bot.SQLRequest(request, commit = True, return_error = True, param = param)

        self.OnChange()
        if error:
            self.m_Log.Error(f'Пользователь {a_UserID}. Ошибка добавления записи в таблицу {request} {param}.')
        else:
            self.m_Log.Success(f'Пользователь {a_UserID}. Добавлена запись в таблицу {request} {param}.')

        return res, error

    def SelectSourceTemplate(self, a_PrevPrefix, a_ButtonName):
        parent_id_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PARENT_ID)
        return bd_item_select.DBItemSelectSource(self.m_Bot, self.m_Table.GetName(), parent_id_field, a_PrevPrefix, a_ButtonName)

    def RegisterSelect(self, a_ButtonName, access_mode, only_parent = False):
        a_Prefix = None
        if self.m_ParentModName:
            parent_mod = self.GetModule(self.m_ParentModName)
            a_Prefix = parent_mod.RegisterSelect(a_ButtonName, access_mode, only_parent = False)

        if not only_parent:
            a_Prefix =  bd_item_select.SelectRegisterHandlers(self.m_Bot, \
                        self.SelectSourceTemplate(a_Prefix, a_ButtonName), \
                        self.m_GetButtonNameAndKeyValueAndAccessFunc, \
                        self.GetMessage(Messages.SELECT), \
                        self.m_GetAccessFunc,\
                        access_mode = access_mode\
                        )

        return a_Prefix

    def AdditionalKeyboardForEditTemplate(self, a_Field):
        if a_Field.m_Type == bd_table.TableFieldType.ENUM:
            def KeyboardButtons(a_Message, a_UserGroups):
                cur_buttons = []
                for s in a_Field.m_Enum:
                    cur_buttons += [keyboard.ButtonWithAccess(self.GetButton(EnumButton(s)), user_access.AccessMode.EDIT, self.GetAccess()),]
                return keyboard.MakeButtons(self.m_Bot, cur_buttons, a_UserGroups)
            return KeyboardButtons
        return None

    def PostProccessingForFieldForEditTemplate(self, a_Field):
        if a_Field.m_Type == bd_table.TableFieldType.ENUM:
            def PostProccessing(a_Message):
                for s in a_Field.m_Enum:
                    if a_Message == str(self.GetButton(EnumButton(s))):
                        return str(s)
                return a_Message
            return PostProccessing
        return None

    async def OnChangeField(self, a_Field, a_ItemID, a_ItemData, a_EditUserID):
        pass

    def RegisterEdit(self, a_Field, a_AccessMode = user_access.AccessMode.EDIT):
            a_ButtonName = self.GetButton(EditButton(a_Field.m_Destiny))
            a_EditMessage = self.GetMessage(EditMessage(a_Field.m_Destiny))
            a_FieldName = a_Field.m_Name

            a_FieldType = bd_item.FieldType.text
            if a_Field.m_Type == bd_table.TableFieldType.PHOTO:
                a_FieldType = bd_item.FieldType.photo

            if not a_ButtonName or not a_EditMessage:
                return

            async def OnChange(a_ItemID, a_ItemData, a_EditUserID):
                await self.OnChangeField(a_Field, a_ItemID, a_ItemData, a_EditUserID)
                return self.OnChange()

            table_name = self.m_Table.GetName()
            key_name = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.KEY)
            edit_keyboard_func = self.m_GetEditKeyboardButtonsFunc
            GetButtonNameAndKeyValueAndAccess = self.m_GetButtonNameAndKeyValueAndAccessFunc
            GetAccess = self.m_GetAccessFunc

            a_Prefix = self.RegisterSelect(a_ButtonName, a_AccessMode, only_parent = True)

            bd_item_edit.EditBDItemRegisterHandlers(self.m_Bot, \
                self.SelectSourceTemplate(a_Prefix, a_ButtonName), \
                MakeFSMForEdit(self.GetName(), a_FieldName), \
                self.GetMessage(Messages.SELECT_TO_EDIT), \
                self.ShowMessageTemplate(a_EditMessage), \
                self.ShowMessageTemplate(self.GetMessage(Messages.SUCCESS_EDIT)), \
                table_name, \
                key_name, \
                a_FieldName, \
                self.PostProccessingForFieldForEditTemplate(a_Field),\
                GetButtonNameAndKeyValueAndAccess, \
                GetAccess, \
                self.AdditionalKeyboardForEditTemplate(a_Field),\
                edit_keyboard_func, \
                OnChange,\
                access_mode = a_AccessMode, \
                field_type = a_FieldType\
                )

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
            self.m_SelectPrefix = a_Prefix
            a_Prefix = bd_item_select.SelectRegisterHandlers(self.m_Bot,\
                    self.SelectSourceTemplate(a_Prefix, a_ButtonName), \
                    GetButtonNameAndKeyValueAndAccess,\
                    self.GetMessage(Messages.SELECT),\
                    GetAccess,\
                    access_mode = user_access.AccessMode.VIEW\
                    )
            bd_item_view.ShowBDItemRegisterHandlers(self.m_Bot,\
                    a_Prefix,\
                    table_name,\
                    key_name,\
                    self.ShowMessageTemplate(self.GetMessage(Messages.OPEN), GetViewItemInlineKeyboardTemplate, a_EnablePhoto = True),\
                    GetAccess,\
                    defaul_keyboard_func,\
                    access_mode = user_access.AccessMode.VIEW\
                    )

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
                    self.ShowMessageTemplate(self.GetMessage(CreateMessage(bd_table.TableFieldDestiny.NAME))), \
                    self.ShowMessageTemplate(self.GetMessage(CreateMessage(bd_table.TableFieldDestiny.DESC))), \
                    self.ShowMessageTemplate(self.GetMessage(CreateMessage(bd_table.TableFieldDestiny.PHOTO))), \
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

        address_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.ADDRESS)
        status_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.STATUS)

        for f in self.m_Table.GetFields():
            self.RegisterEdit(f)

    def OnChange(self):
        pass
