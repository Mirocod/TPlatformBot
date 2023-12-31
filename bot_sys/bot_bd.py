#-*-coding utf-8-*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

import sqlite3
from bot_sys import log

# Работа с базой данных

def GetBDDateTimeNow():
    return 'datetime(\'now\')'

def SelectBDTemplate(a_Bot, a_TableName):
    def SelectBD():
        return a_Bot.SQLRequest(f'SELECT * FROM {a_TableName}')
    return SelectBD

def RequestSelectTemplate(a_Bot, a_TableName):
    def SelectBD():
        return a_Bot.SQLRequest(f'SELECT * FROM {a_TableName}')
    return SelectBD

def SQLRequest(a_Log, a_BDFileName, a_Request : str, commit = False, return_error = False, param = None):
    db = sqlite3.connect(a_BDFileName)
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
        a_Log.Error(f'Ошибка при обработке запроса [{a_Request}]:{str(e)}')
        error = "Ошибка sqlite3:" + str(e)
    cursor.close()
    db.close()
    if not error and commit: 
        a_Log.Success(f'Выполнен запрос [{a_Request}]')
    if return_error:
        return result, error
    return result
