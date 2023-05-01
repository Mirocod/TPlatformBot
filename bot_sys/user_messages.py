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

g_last_update = None
def UpdateSignal(a_DateTime):
    global g_last_update
    g_last_update = a_DateTime
# ---------------------------------------------------------
# Функции работы с собщениями

# ---------------------------------------------------------
class Message:
    def __init__(self, a_MessageName : str, a_MessageDesc : str, a_Language : str, a_PhotoID : str, a_DateTime):
        self.m_MessageName = a_MessageName
        self.m_MessageDesc = a_MessageDesc
        self.m_Language = a_Language
        self.m_PhotoID = a_PhotoID
        self.m_DateTime = a_DateTime

    def __str__(self):
        global g_last_update
        last_update = g_last_update
        if self.m_DateTime < last_update:
            msg = GetMessages()
            if not msg.get(self.m_Language, None):
                msg[self.m_Language] = {}
            new_msg = msg[self.m_Language].get(self.m_MessageName, self)
            self.m_MessageName = new_msg.m_MessageName
            self.m_MessageDesc = new_msg.m_MessageDesc
            self.m_PhotoID = new_msg.m_PhotoID
            self.m_DateTime = last_update
        return f'{self.m_MessageDesc}'

def MSG(a_MessageName, a_MessageDesc, a_UpdateMSG, a_DateTime):
    cur_msg = Message(a_MessageName, a_MessageDesc, default_language, 0, a_DateTime)
    msg = GetMessages()
    if not msg.get(default_language, None):
        msg[default_language] = {}
    if not msg[default_language].get(a_MessageName, None):
        msg[default_language][a_MessageName] = cur_msg
    a_UpdateMSG(cur_msg)

