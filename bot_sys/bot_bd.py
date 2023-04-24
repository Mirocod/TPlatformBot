#-*-coding utf-8-*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

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

def BDExecute(a_Commands):
    db = sqlite3.connect(GetBDFileName())
    cursor = db.cursor()
    for cmd in a_Commands:
        print(cmd)
        cursor.execute(cmd)
    db.commit()
    cursor.close()
    db.close()

def SelectBDTemplate(a_TableName):
    def SelectBD():
        return SQLRequestToBD(f'SELECT * FROM {a_TableName}')
    return SelectBD

def SQLRequestToBDCommit(a_Request : str):
    return SQLRequestToBD1Commit(a_Request, None)

def SQLRequestToBD1Commit(a_Request : str, a_Param1):
    return SQLRequestToBD2Commit(a_Request, a_Param1, None)

def SQLRequestToBD2Commit(a_Request : str, a_Param1, a_Param2):
    return SQLRequestToBD3Common(a_Request, True, a_Param1, a_Param2, None)

def SQLRequestToBD3Commit(a_Request : str, a_Param1, a_Param2, a_Param3):
    return SQLRequestToBD3Common(a_Request, True, a_Param1, a_Param2, a_Param3)

def SQLRequestToBD(a_Request : str):
    return SQLRequestToBD1(a_Request, None)

def SQLRequestToBD1(a_Request : str, a_Param1):
    return SQLRequestToBD2(a_Request, a_Param1, None)

def SQLRequestToBD2(a_Request : str, a_Param1, a_Param2):
    return SQLRequestToBD3Common(a_Request, False, a_Param1, a_Param2, None)

def SQLRequestToBD3(a_Request : str, a_Param1, a_Param2, a_Param3):
    return SQLRequestToBD3Common(a_Request, False, a_Param1, a_Param2, a_Param3)

def SQLRequestToBD3Common(a_Request : str, a_Commit : bool, a_Param1, a_Param2, a_Param3):
    db = sqlite3.connect(GetBDFileName())
    cursor = db.cursor()
    result = []
    try:
        if not a_Param3 is None:
            cursor.execute(a_Request, (a_Param1, a_Param3, a_Param3))
        elif not a_Param2 is None:
            cursor.execute(a_Request, (a_Param1, a_Param2))
        elif not a_Param1 is None:
            cursor.execute(a_Request, (a_Param1))
        else:
            cursor.execute(a_Request)
        result = cursor.fetchall()
        if a_Commit: 
            db.commit()
    except sqlite3.Error as e:
        log.Error(f'Ошибка при обработке запроса [{a_Request}]:{str(e)}')
        result = "Ошибка sqlite3:" + str(e)
    cursor.close()
    db.close()
    return result
