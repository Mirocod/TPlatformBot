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
# Первичаня иницилизация базы данных

# Открываем БД, если её нет, то создаём
db = sqlite3.connect(GetBDFileName())
cursor = db.cursor()

# Таблица пользователей
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER,
    userName TEXT,
    UNIQUE(user_id)
);""")

# Таблица групп пользователей
cursor.execute("""CREATE TABLE IF NOT EXISTS group1(
    group_id INTEGER,
    groupName TEXT,
    UNIQUE(group_id)
);""")

# Таблица соответствия пользователей и групп пользователей
cursor.execute("""CREATE TABLE IF NOT EXISTS groups_users1(
    user_id INTEGER,
    group_id INTEGER
);""")

db.commit()
cursor.close()
db.close()
