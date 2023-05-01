#-*-coding utf-8-*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

import sqlite3
from bot_sys import log

# Работа ссообщениями

default_language = 'ru'

g_messages = None
def GetMessages():
    global g_messages
    if not g_messages:
        g_messages = {}
    return g_messages

# ---------------------------------------------------------
# Функции работы с собщениями

# ---------------------------------------------------------
class Message:
    def __init__(self, a_MessageName : str, a_MessageDesc : str, a_Language : str, a_PhotoID : str):
        self.m_MessageName = a_MessageName
        self.m_MessageDesc = a_MessageDesc
        self.m_Language = a_Language
        self.m_PhotoID = a_PhotoID
    def __str__(self):
        return f'{self.m_MessageDesc}'

def MSG(a_MessageName, a_MessageDesc, a_UpdateMSG):
    cur_msg = Message(a_MessageName, a_MessageDesc, default_language, 0)
    msg = GetMessages()
    if not msg.get(default_language, None):
        msg[default_language] = {}
    if not msg[default_language].get(a_MessageName, None):
        msg[default_language][a_MessageName] = cur_msg
    a_UpdateMSG(cur_msg)

def UpdateMSG(a_Message : Message):
    print(a_Message.m_MessageName, a_Message.m_MessageDesc)
    globals()[a_Message.m_MessageName] = a_Message
