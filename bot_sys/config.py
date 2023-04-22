#-*-coding utf-8-*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Настнойка основных параметров системы

# ---------------------------------------------------------
# API токен телеграмм бота. Создаётся с помощью @BotFather
# Задаётся либо прямо тут в коде, либо в файле telegram_bot_api_token_file_name
g_telegram_bot_api_token = ''

# Пользователи имеющие полный доступ, ID можно узнать например у этого бота @GetMyIDBot
# Задаётся либо прямо тут в коде, либо в файле root_ids_file_name
g_root_ids = []

# Логирование событий в файл
g_log_to_file = True

# ---------------------------------------------------------
# Файлы для настройки, которые не коммитятся в git
telegram_bot_api_token_file_name = 'config_telegram_bot_api_token'
root_ids_file_name = 'config_root_ids'

# ---------------------------------------------------------
# Дополнительные функции

def ClearReadLine(a_Line):
    return a_Line[:-1]

def GetFirstLineFromFile(a_FileName):
    f = open(a_FileName, 'r')
    result = f.readline() 
    f.close()
    return result

def GetAllLinesFromFile(a_FileName):
    f = open(a_FileName, 'r')
    result = f.readlines() 
    f.close()
    return result

# ---------------------------------------------------------
# Основные функции

def GetTelegramBotApiToken():
    global g_telegram_bot_api_token
    if len(g_telegram_bot_api_token) == 0:
        g_telegram_bot_api_token = ClearReadLine(GetFirstLineFromFile(telegram_bot_api_token_file_name))

    return g_telegram_bot_api_token

def GetRootIDs():
    global g_root_ids
    if len(g_root_ids) == 0:
        root_ids = GetAllLinesFromFile(root_ids_file_name)
        for i in root_ids:
            g_root_ids += [ClearReadLine(i)]

    return g_root_ids

