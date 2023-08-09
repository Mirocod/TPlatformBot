# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

import os

from bot_sys import config, log, aiogram_bot, bot_messages, bd_table, user_access
from bot_modules import mod_agregator, start, profile, backup, users_groups_agregator, access, projects, tasks, needs, comments
from bot_modules import languages, messages, buttons, users, groups, user_in_groups
from bot_modules import orders, all_orders
from bot_modules import bd_version

from bot_sys import bot_subscribes
from bot_modules import subscribes

log_start_message = 'Бот успешно запущен!'

bd_file_name = 'bot.db'

log_file_name = 'log.txt'

default_language = 'ru'

g_Log = log.Log(log_file_name)
g_Bot = aiogram_bot.AiogramBot(config.GetTelegramBotApiToken(), bd_file_name, config.GetRootIDs(), g_Log)

g_BotMessages = bot_messages.BotMessages(default_language)
g_BotButtons = bot_messages.BotMessages(default_language)
g_BotSubscribes = bot_subscribes.BotSubscribes()

g_ModuleAgregator = mod_agregator.ModuleAgregator()

mod_start_name = start.module_name
mod_tasks_name = tasks.module_name
mod_needs_name = needs.module_name
mod_comments_name = comments.module_name
mod_projects_name = projects.module_name
mod_languages_name = languages.module_name
mod_messages_name = messages.module_name
mod_buttons_name = buttons.module_name
mod_users_name = users.module_name
mod_groups_name = groups.module_name
mod_user_in_groups_name = user_in_groups.module_name
mod_orders_name = orders.module_name
mod_all_orders_name = all_orders.module_name

start_mod_list = [mod_start_name]
mod_access = access.ModuleAccess(start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_access)

mod_users = users.ModuleUsers(None, None, start_mod_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_users)

child_mod_name_list = [mod_start_name, mod_users_name, mod_user_in_groups_name]
mod_groups = groups.ModuleGroups(None, mod_user_in_groups_name, child_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_groups)

mod_user_in_groups = user_in_groups.ModuleUserInGroups(mod_groups_name, None, start_mod_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_user_in_groups)

child_mod_name_list = [mod_start_name, mod_users_name, mod_groups_name, mod_user_in_groups_name]
mod_users_groups_agregator = users_groups_agregator.ModuleUsersGroupsAgregator(child_mod_name_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_users_groups_agregator)

mod_profile = profile.ModuleProfile(start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_profile)

mod_backup = backup.ModuleBackup(start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_backup)

child_mod_name_list = [mod_start_name, mod_tasks_name, mod_needs_name, mod_comments_name]
mod_project = projects.ModuleProjects(None, mod_tasks_name, child_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_project)

child_mod_name_list = [mod_start_name]#, mod_projects_name, mod_needs_name, mod_comments_name]
mod_tasks = tasks.ModuleTasks(mod_projects_name, mod_needs_name, child_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_tasks)

child_mod_name_list = [mod_start_name]#, mod_projects_name, mod_tasks_name, mod_comments_name]
mod_needs= needs.ModuleNeeds(mod_tasks_name, mod_comments_name, child_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_needs)

child_mod_name_list = [mod_start_name]#, mod_projects_name, mod_tasks_name, mod_needs_name]
mod_comments= comments.ModuleComments(mod_needs_name, None, child_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_comments)

child_mod_name_list = [mod_start_name, mod_messages_name, mod_buttons_name]
mod_languages = languages.ModuleLanguages(None, mod_messages_name, child_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_languages)

child_mod_name_list = [mod_start_name]
mod_messages = messages.ModuleMessages(mod_languages_name, None, child_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_messages)

child_mod_name_list = [mod_start_name]
mod_buttons = buttons.ModuleButtons(mod_languages_name, None, child_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_buttons)

child_mod_name_list = [mod_start_name]
mod_orders = orders.ModuleUserOrders(None, None, child_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_orders)

child_mod_name_list = [mod_start_name]
mod_all_orders = all_orders.ModuleAllOrders(None, None, child_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_all_orders)

child_mod_name_list = [mod_start_name]
mod_subscribe = subscribes.ModuleUserSubscribe(None, None, child_mod_name_list, start_mod_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_subscribe)

mod_bd_version = bd_version.ModuleBDVersion(g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
g_ModuleAgregator.AddModule(mod_bd_version)

child_mod_name_list = [
        mod_profile.GetName(),
        mod_backup.GetName(),
        mod_users_groups_agregator.GetName(),
        mod_access.GetName(),
        mod_project.GetName(),
        mod_languages.GetName(),
        mod_orders.GetName(),
        mod_all_orders.GetName(),
        mod_subscribe.GetName(),
        mod_bd_version.GetName(),
        ]
mod_start = start.ModuleStart(child_mod_name_list, g_Bot, g_ModuleAgregator, g_BotMessages, g_BotButtons, g_BotSubscribes, g_Log)
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
test_mods = [user_access, bd_table, bot_subscribes]
for m in test_mods:
    m.Test()

if __name__ == '__main__':
    #os.system('clear')
    #os.system('cls')
    g_Log.Success(log_start_message)

g_Bot.StartPolling()
