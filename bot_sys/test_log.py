#-*-coding utf-8-*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# ---------------------------------------------------------
# Логирование событий в список

# Четыре типа уведомлений:
# Info        - Информация.
# Warn      - Предупреждение.
# Error      - Ошибка.
# Success - Успех.

class TestLog:
    def __init__(self):
        self.m_LogMessage = []

    def GetLogMessage():
        result = self.m_LogMessage
        self.m_LogMessage = []
        return result

    def GetFileName(self):
        return self.m_FileName

    def GetTimeNow(self):
        return datetime.datetime.now()

    def GetTime(self):
        now = self.GetTimeNow()
        time = now.strftime(f"[%d.%m.%Y, %H:%M]")
        return time

    def Info(self, a_LogMessage):
        time = self.GetTime()
        self.WriteToList(f'{time} | {a_LogMessage}')

    def Warn(self, a_LogMessage):
        time = self.GetTime()
        self.WriteToList(f'{time} | {a_LogMessage}')
    
    def Error(self, a_LogMessage):
        time = self.GetTime()
        self.WriteToList(f'{time} | {a_LogMessage}')

    def Success(self, a_LogMessage):
        time = self.GetTime()
        self.WriteToList(f'{time} | {a_LogMessage}')

    def WriteToList(self, a_LogMessage):
        self.m_LogMessage += [a_LogMessage]

