#-*-coding utf-8-*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

import sqlite3
from bot_sys import log

# Работа с базой данных

# Имя файла БД
g_bd_file_name = 'bot.db'
def GetBDFileName():
    return g_bd_file_name

# ---------------------------------------------------------
# Функции работы с базой

# ---------------------------------------------------------

def GetBDDateTimeNow():
    return 'datetime(\'now\')'

def BDExecute(a_Commands):
    for cmd in a_Commands:
        SQLRequestToBD(cmd, commit = True)

def SelectBDTemplate(a_TableName):
    def SelectBD():
        return SQLRequestToBD(f'SELECT * FROM {a_TableName}')
    return SelectBD

def SQLRequestToBD(a_Request : str, commit = False, return_error = False, param = None):
    db = sqlite3.connect(GetBDFileName())
    cursor = db.cursor()
    result = []
    error = None
    try:
        if not param is None:
            cursor.execute(a_Request, (param))
        else:
            cursor.execute(a_Request)
        result = cursor.fetchall()
        if commit: 
            db.commit()
    except sqlite3.Error as e:
        log.Error(f'Ошибка при обработке запроса [{a_Request}]:{str(e)}')
        error = "Ошибка sqlite3:" + str(e)
    cursor.close()
    db.close()
    if not error: log.Success(f'Выполнен запроса [{a_Request}]')
    if return_error:
        return result, error
    return result
