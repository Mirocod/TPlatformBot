#-*-coding utf-8-*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

import sqlite3

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

'''
# Таблица групп пользователей
cursor.execute("""CREATE TABLE IF NOT EXISTS group(
    group_id INTEGER,
    groupName TEXT,
    UNIQUE(group_id)
);""")

# Таблица соответствия пользователей и групп пользователей
cursor.execute("""CREATE TABLE IF NOT EXISTS groups_users(
    user_id INTEGER,
    group_id INTEGER
);""")
'''

