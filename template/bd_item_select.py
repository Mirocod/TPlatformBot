# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Просмотр элемента в БД

from bot_sys import user_access, bot_bd, keyboard
from bot_modules import access_utils, groups_utils
from template import simple_message, bd_item

from abc import ABC, abstractmethod

def GetCustomListKeyboardButtonsTemplate(a_Bot, a_GetItemsFunc, a_PrevPrefix, a_NextPrefix : str, a_GetButtonNameAndKeyValueAndAccessFunc, access_mode = user_access.AccessMode.VIEW):
    def GetBDItemsListKeyboardButtons(a_Message, a_UserGroups):
        parent_id = bd_item.GetKeyDataFromCallbackMessage(a_Message, a_PrevPrefix)
        items = a_GetItemsFunc(a_Message, a_UserGroups, parent_id)

        items_button_list = []
        for t in items:
            bname, key_value, access = a_GetButtonNameAndKeyValueAndAccessFunc(t)
            if access is None:
                access = ''
            if bname:
                b = keyboard.InlineButtonWithAccess(bname, a_NextPrefix, key_value, access, access_mode)
                items_button_list += [b]
        return keyboard.MakeInlineKeyboardButtons(a_Bot, items_button_list, a_UserGroups)
    return GetBDItemsListKeyboardButtons

def GetBDItemsTemplate(a_Bot, a_TableName : str, a_ParentIDFieldName):
    def GetBDItems(a_Message, a_UserGroups, a_ParentID):
        items = []
        if a_ParentIDFieldName and a_ParentID and a_ParentID != '':
            items = bd_item.GetBDItemsTemplate(a_Bot, a_TableName, a_ParentIDFieldName)(a_ParentID)
        else:
            items = bd_item.GetAllItemsTemplate(a_Bot, a_TableName)()

        return items
    return GetBDItems

def SelectCustomTemplate(a_Bot, a_GetItemsFunc, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_PrevPrefix, a_NextPrefix, access_mode = user_access.AccessMode.VIEW):
    inline_keyboard_func = GetCustomListKeyboardButtonsTemplate(a_Bot, a_GetItemsFunc, a_PrevPrefix, a_NextPrefix, a_GetButtonNameAndKeyValueAndAccessFunc)
    return simple_message.InfoMessageTemplate(a_Bot, a_StartMessage, None, inline_keyboard_func, a_AccessFunc, access_mode)

class ISelectSource(ABC):
    @abstractmethod
    def IsFirst(self):
        pass

    @abstractmethod
    def GetItemsFunc(self):
        pass

    @abstractmethod
    def GetCheckFunc(self):
        pass

    @abstractmethod
    def GetPrevPrefix(self):
        pass

    @abstractmethod
    def GetPrefixBase(self):
        pass

class DBItemSelectSource:
    def __init__(self, a_Bot, a_TableName, a_ParentIDFieldName, a_PrevPrefix, a_ButtonName):
        self.a_Bot = a_Bot
        self.a_TableName = a_TableName
        self.a_ParentIDFieldName = a_ParentIDFieldName
        self.a_PrevPrefix = a_PrevPrefix
        self.a_ButtonName = a_ButtonName

    def IsFirst(self):
        return not self.a_ParentIDFieldName

    def GetItemsFunc(self):
        return GetBDItemsTemplate(self.a_Bot, self.a_TableName, self.a_ParentIDFieldName)

    def GetCheckFunc(self):
        if self.IsFirst():
            return bd_item.GetCheckForTextFunc(a_ButtonName)
        return bd_item.GetCheckForPrefixFunc(a_PrevPrefix)

    def GetPrevPrefix(self):
        return self.a_PrevPrefix

    def GetPrefixBase(self):
        if self.a_PrevPrefix:
            return self.a_PrevPrefix
        return self.a_ButtonName

def SelectRegisterHandlers(a_Bot, a_SelectSource, a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, access_mode = user_access.AccessMode.VIEW):
    reg_func = a_Bot.RegisterMessageHandler
    if not a_SelectSource.IsFirst():
        reg_func = a_Bot.RegisterCallbackHandler

    a_NextPrefix = bd_item.HashPrefix(f'select_{a_SelectSource}_after_prefix_or_in_base_{a_SelectSource.GetPrefixBase()}:')

    sel_handler = SelectCustomTemplate(a_Bot, a_SelectSource.GetItemsFunc(), a_GetButtonNameAndKeyValueAndAccessFunc, a_StartMessage, a_AccessFunc, a_SelectSource.GetPrevPrefix(), a_NextPrefix, access_mode = access_mode)
    reg_func(sel_handler, a_SelectSource.GetCheckFunc())

    return a_NextPrefix

