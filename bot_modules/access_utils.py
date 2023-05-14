# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Права пользователей

from bot_sys import bot_bd

# ---------------------------------------------------------
# БД
table_name = 'module_access'
mod_name_field = 'modName'
moduleaccess_field = 'modAccess'
mod_default_access_field = 'itemDefaultAccess'

access_denied_message = '''
❌ Доступ запрещён!
''' 

def GetAccessForModuleRequest(module_name, access, default_access):
    return f"INSERT OR IGNORE INTO {table_name} ({mod_name_field}, {moduleaccess_field}, {mod_default_access_field}) VALUES ('{module_name}', '{access}', '{default_access}');"

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
