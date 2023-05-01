#-*-coding utf-8-*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# ---------------------------------------------------------
# Логирование событий в файл

# Четыре типа уведомлений:
# Info        - Информация.
# Warn      - Предупреждение.
# Error      - Ошибка.
# Success - Успех.

# Файл лога
g_log_file_name = 'log.txt'

from bot_sys import config
import colorama
import datetime
colorama.init()

def GetTimeNow():
    return datetime.datetime.now()

def GetTime():
    now = GetTimeNow()
    time = now.strftime(f"[%d.%m.%Y, %H:%M]")
    return time

def Info(a_LogMessage):
    time = GetTime()
    WriteToFile(f'{time} | {a_LogMessage}')
    print(f"{time} {colorama.Back.BLUE}{colorama.Style.BRIGHT} ИНФО {colorama.Style.RESET_ALL} | {a_LogMessage}")

def Warn(a_LogMessage):
    time = GetTime()
    WriteToFile(f'{time} | {a_LogMessage}')
    print(f"{time} {colorama.Back.YELLOW}{colorama.Style.BRIGHT} ВНИМАНИЕ {colorama.Style.RESET_ALL} | {a_LogMessage}")

def Error(a_LogMessage):
    time = GetTime()
    WriteToFile(f'{time} | {a_LogMessage}')
    print(f"{time} {colorama.Back.RED}{colorama.Style.BRIGHT} ОШИБКА {colorama.Style.RESET_ALL} | {a_LogMessage}")

def Success(a_LogMessage):
    time = GetTime()
    WriteToFile(f'{time} | {a_LogMessage}')
    print(f"{time} {colorama.Back.GREEN}{colorama.Style.BRIGHT} УСПЕХ {colorama.Style.RESET_ALL} | {a_LogMessage}")

def WriteToFile(a_LogMessage):
    if config.g_log_to_file != True:
        return

    f = open(g_log_file_name, 'a+')
    f.write(a_LogMessage)
    f.write('\n')
    f.close()

