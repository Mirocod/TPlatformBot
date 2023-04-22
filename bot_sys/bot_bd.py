#-*-coding utf-8-*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

import sqlite3

# Работа с базой данных

# Имя файла БД
g_bd_file_name = 'bot.db'

# ---------------------------------------------------------
# Первичаня иницилизация базы данных

# Открываем БД, если её нет, то создаём
db = sqlite3.connect(g_bd_file_name)
cursor = db.cursor()

# Таблица пользователей
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER,
    userName TEXT,
    UNIQUE(user_id)
)""")

# Таблица групп пользователей
cursor.execute("""CREATE TABLE IF NOT EXISTS group(
    group_id INTEGER,
    groupName TEXT,
    UNIQUE(group_id)
)""")

db.commit()
cursor.close()
db.close()
