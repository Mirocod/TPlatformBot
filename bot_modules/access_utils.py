# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Права пользователей. Утилиты

table_name = 'module_access'
mod_name_field = 'modName'
moduleaccess_field = 'modAccess'
mod_default_access_field = 'itemDefaultAccess'

def GetAccessForModuleRequest(module_name, access, default_access):
     return f"INSERT OR IGNORE INTO {table_name} ({mod_name_field}, {moduleaccess_field}, {mod_default_access_field}) VALUES ('{module_name}', '{access}', '{default_access}');"
