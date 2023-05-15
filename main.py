# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

log_start_message = 'Бот успешно запущен!'

import os

from bot_sys import config, log, bot_bd, user_access, aiogram_bot, bot_messages, bd_table
from bot_modules import mod_agregator, start, profile, backup, groups, access #, projects, , access, , tasks, needs, comments, messages, , languages

g_Log = log
g_Bot = aiogram_bot.AiogramBot(config.GetTelegramBotApiToken(), bot_bd.GetBDFileName(), config.GetRootIDs(), g_Log)

default_language = 'ru'

g_BotMessages = bot_messages.BotMessages(default_language)
g_BotButtons = bot_messages.BotMessages(default_language)

g_ModuleAgregator = mod_agregator.ModuleAgregator()

mod_start_name = 'start'

mod_access = access.ModuleAccess([mod_start_name], g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_access)

mod_groups = groups.ModuleGroups([mod_start_name], g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_groups)

mod_profile = profile.ModuleProfile([mod_start_name], g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_profile)

mod_backup = backup.ModuleBackup([mod_start_name], g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_backup)

start_mod_name_list = [#, 'projects', 'groups', 'access', , 'languages']
        mod_profile.GetName(),
        mod_backup.GetName(),
        mod_groups.GetName(),
        mod_access.GetName(),
        ]
mod_start = start.ModuleStart(start_mod_name_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_start)

# Первичная инициализация модулей. Все модули должны быть прописаны в списке modules
modules = g_ModuleAgregator.GetModList() # [start] #tasks, access, profile, projects, groups, backup, needs, comments, messages, languages]

init_bd_cmds = []
for m in modules:
    c = m.GetInitBDCommands()
    if not c is None:
        init_bd_cmds += c
# Первичная инициализация базы данных
for c in init_bd_cmds:
    g_Bot.SQLRequest(c, commit = True)

g_BotMessages.UpdateSignal(g_Log.GetTimeNow())
g_BotButtons.UpdateSignal(g_Log.GetTimeNow())

#languages.FlushLanguages()
#messages.FlushMessages()

for m in modules:
    print(m)
    m.RegisterHandlers()

# Юнит тесты модулей и файлов
test_mods = [user_access, bd_table]
for m in test_mods:
    m.Test()

if __name__ == '__main__':
#    os.system('clear')
#    os.system('cls')
    g_Log.Success(log_start_message)

g_Bot.StartPolling()
