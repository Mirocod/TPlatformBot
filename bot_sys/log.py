#-*-coding utf-8-*-
# Общественное достояние 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# ---------------------------------------------------------
# Логирование событий в файл

# Четыре типа уведомлений:
# Info        - Информация.
# Warn      - Предупреждение.
# Error      - Ошибка.
# Success - Успех.

import colorama
import datetime
colorama.init()

# TODO: Сообщения в файл не различются по Info Warn Error Success . Нужно добавить чтобы они различались
class Log:
    def __init__(self, a_FileName):
        self.m_FileName = a_FileName

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
        self.WriteToFile(f'{time} | {a_LogMessage}')
        print(f"{time} {colorama.Back.BLUE}{colorama.Style.BRIGHT} ИНФО {colorama.Style.RESET_ALL} | {a_LogMessage}")

    def Warn(self, a_LogMessage):
        time = self.GetTime()
        self.WriteToFile(f'{time} | {a_LogMessage}')
        print(f"{time} {colorama.Back.YELLOW}{colorama.Style.BRIGHT} ВНИМАНИЕ {colorama.Style.RESET_ALL} | {a_LogMessage}")
    
    def Error(self, a_LogMessage):
        time = self.GetTime()
        self.WriteToFile(f'{time} | {a_LogMessage}')
        print(f"{time} {colorama.Back.RED}{colorama.Style.BRIGHT} ОШИБКА {colorama.Style.RESET_ALL} | {a_LogMessage}")

    def Success(self, a_LogMessage):
        time = self.GetTime()
        self.WriteToFile(f'{time} | {a_LogMessage}')
        print(f"{time} {colorama.Back.GREEN}{colorama.Style.BRIGHT} УСПЕХ {colorama.Style.RESET_ALL} | {a_LogMessage}")

    def WriteToFile(self, a_LogMessage):
        if not self.m_FileName:
            return
    
        f = open(self.m_FileName, 'a+')
        f.write(a_LogMessage)
        f.write('\n')
        f.close()

