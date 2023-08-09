# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Версия БД
# Этот модуль нужен для того, чтобы проводить миграции на новую версию. Он записывает в БД номер текущей версии.


from bot_sys import bot_bd, keyboard, user_access, bd_table, bot_subscribes
from bot_modules import mod_table_operate, mod_simple_message

# ---------------------------------------------------------
# БД
module_name = 'bd_version'

table_name = module_name
base_version_number_field = 'baseVersionNumber'
sub_version_number_field = 'subVersionNumber'

table_base_version_number_field = bd_table.TableField(base_version_number_field, bd_table.TableFieldDestiny.VERSION_NUMBER, bd_table.TableFieldType.INT)
table_sub_version_number_field = bd_table.TableField(sub_version_number_field, bd_table.TableFieldDestiny.SUB_VERSION_NUMBER, bd_table.TableFieldType.INT)

table = bd_table.Table(table_name, [
        table_base_version_number_field,
        table_sub_version_number_field,
        ],
        [
            [table_base_version_number_field, table_sub_version_number_field],
        ])

init_access = f'{user_access.user_access_group_new}=-'

# ---------------------------------------------------------
# Сообщения и кнопки

button_names = {
}

messages = {
}

class ModuleBDVersion(mod_table_operate.TableOperateModule):
    def __init__(self, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_BotSubscribes, a_Log):
        super().__init__(table, messages, button_names, None, None, init_access, None, None, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_BotSubscribes, a_Log)

    def GetName(self):
        return module_name

    def GetInitBDCommands(self):
        return super(). GetInitBDCommands() + [
            f"INSERT OR IGNORE INTO {table_name} ({base_version_number_field}, {sub_version_number_field}) VALUES ('{1}', '{0}');"
            ]
