# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Права пользователей. Утилиты

from bot_sys import user_access, bot_bd

table_name = 'module_access'
mod_name_field = 'modName'
moduleaccess_field = 'modAccess'
mod_default_access_field = 'itemDefaultAccess'

def GetAccessForModuleRequest(module_name, access, default_access):
     return f"INSERT OR IGNORE INTO {table_name} ({mod_name_field}, {moduleaccess_field}, {mod_default_access_field}) VALUES ('{module_name}', '{access}', '{default_access}');"

def GetUserGroupData(a_Bot, a_UserID):
    def GetGroupNamesForUser(a_UserID):
        return a_Bot.SQLRequest('SELECT groupName FROM user_groups WHERE group_id=(SELECT group_id FROM user_in_groups WHERE user_id = ?)', param = [a_UserID])
    r = GetGroupNamesForUser(a_UserID)
    groups = []
    for i in r:
        if len(i) > 0:
            groups += [i[0]]
    return user_access.UserGroups(a_UserID, groups)

def GetModulesAccessList(a_Bot):
    return bot_bd.RequestSelectTemplate(a_Bot.m_BDFileName, table_name)()

def GetAccessForModule(a_Bot, a_ModuleName):
    alist = GetModulesAccessList(a_Bot)
    for i in alist:
        if i[0] == a_ModuleName:
            return i[1]
    return ''

def GetItemDefaultAccessForModule(a_Bot, a_ModuleName):
    alist = GetModulesAccessList(a_Bot)
    for i in alist:
        if i[0] == a_ModuleName:
            return i[2]
    return ''
