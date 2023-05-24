# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

import os

from bot_sys import config, log, aiogram_bot, bot_messages, bd_table, user_access
from bot_modules import mod_agregator, start, profile, backup, users_groups_agregator, access, projects, tasks, needs, comments, languages, messages, buttons

log_start_message = 'Бот успешно запущен!'

bd_file_name = 'bot.db'

log_file_name = 'log.txt'

default_language = 'ru'

g_Log = log.Log(log_file_name)
g_Bot = aiogram_bot.AiogramBot(config.GetTelegramBotApiToken(), bd_file_name, config.GetRootIDs(), g_Log)

g_BotMessages = bot_messages.BotMessages(default_language)
g_BotButtons = bot_messages.BotMessages(default_language)

g_ModuleAgregator = mod_agregator.ModuleAgregator()

mod_start_name = start.module_name
mod_tasks_name = tasks.module_name
mod_needs_name = needs.module_name
mod_comments_name = comments.module_name
mod_projects_name = projects.module_name
mod_languages_name = languages.module_name
mod_messages_name = messages.module_name
mod_buttons_name = buttons.module_name

start_mod_list = [mod_start_name]
mod_access = access.ModuleAccess(start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_access)

start_mod_name_list = [mod_start_name]
mod_groups = users_groups_agregator.ModuleUsersGroupsAgregator(start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_groups)

start_mod_list = [mod_start_name]
mod_profile = profile.ModuleProfile(start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_profile)

mod_backup = backup.ModuleBackup(start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_backup)

start_mod_name_list = [mod_start_name, mod_tasks_name, mod_needs_name, mod_comments_name]
mod_project = projects.ModuleProjects(None, mod_tasks_name, start_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_project)

start_mod_name_list = [mod_start_name]#, mod_projects_name, mod_needs_name, mod_comments_name]
mod_tasks = tasks.ModuleTasks(mod_projects_name, mod_needs_name, start_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_tasks)

start_mod_name_list = [mod_start_name]#, mod_projects_name, mod_tasks_name, mod_comments_name]
mod_needs= needs.ModuleNeeds(mod_tasks_name, mod_comments_name, start_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_needs)

start_mod_name_list = [mod_start_name]#, mod_projects_name, mod_tasks_name, mod_needs_name]
mod_comments= comments.ModuleComments(mod_needs_name, None, start_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_comments)

start_mod_name_list = [mod_start_name, mod_messages_name, mod_buttons_name]
mod_languages = languages.ModuleLanguages(None, mod_messages_name, start_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_languages)

start_mod_name_list = [mod_start_name]
mod_messages = messages.ModuleMessages(mod_languages_name, None, start_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_messages)

start_mod_name_list = [mod_start_name]
mod_buttons = buttons.ModuleButtons(mod_languages_name, None, start_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_buttons)

start_mod_name_list = [
        mod_profile.GetName(),
        mod_backup.GetName(),
        mod_groups.GetName(),
        mod_access.GetName(),
        mod_project.GetName(),
        mod_languages.GetName(),
        ]
mod_start = start.ModuleStart(start_mod_name_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_Log)
g_ModuleAgregator.AddModule(mod_start)

# Первичная инициализация модулей.
modules = g_ModuleAgregator.GetModList() 

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

mod_languages.FlushLanguages()
mod_messages.FlushMessages()
mod_buttons.FlushMessages()

for m in modules:
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
