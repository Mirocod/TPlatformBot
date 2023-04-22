#-*-coding utf-8-*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

from bot_sys import bot_bd

import sqlite3

# Работа с базой данных пользователей

# Добавление пользователя, если он уже есть, то игнорируем
def AddUser(a_UserID, a_UserName):
    db = sqlite3.connect(bot_bd.GetBDFileName())
    cursor = db.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, userName) VALUES (?, ?);", (a_UserID, a_UserName));
    db.commit()
    cursor.close()
    db.close()

# Добавление пользователя, если он уже есть, то игнорируем
def GetUserInfo(a_UserID):
    db = sqlite3.connect(bot_bd.GetBDFileName())
    cursor = db.cursor()
    user_info = cursor.execute('SELECT * FROM users WHERE user_id = ?', ([a_UserID])).fetchall()
    cursor.close()
    db.close()
    if len(user_info) != 0:
        return user_info[0]
    return None

