#-*-coding utf-8-*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Работа с сообщениями

class BotMessage:
    def __init__(self, a_BotMessages, a_MessageName : str, a_MessageDesc : str, a_Language : str, a_PhotoID : str, a_DateTime):
        self.m_BotMessages = a_BotMessages
        self.m_MessageName = a_MessageName
        self.m_MessageDesc = a_MessageDesc
        self.m_Language = a_Language
        self.m_PhotoID = a_PhotoID
        self.m_DateTime = a_DateTime

    def StaticCopy(self):
        return BotMessage(None, self.m_MessageName, self.m_MessageDesc, self.m_Language, self.m_PhotoID, self.m_DateTime)

    def GetName(self):
        return self.m_MessageName

    def GetDesc(self):
        return self.m_MessageDesc

    def UpdateDesc(self, a_Desc):
        self.m_MessageDesc = a_Desc

    def GetLanguage(self):
        return self.m_Language

    def GetPhotoID(self):
        return self.m_PhotoID

    def UpdatePhotoID(self, a_PhotoID):
        self.m_PhotoID = a_PhotoID

    def __str__(self):
        msg = self.GetMessageForLang(self.m_Language)
        return msg.GetDesc()

    def GetMessageForLang(self, a_Language):
        if not self.m_BotMessages:
            return self
        last_update = self.m_BotMessages.m_LastUpdate
        new_msg = self
        if self.m_DateTime < last_update:
            msg = self.m_BotMessages.GetMessages()
            if not msg.get(a_Language, None):
                a_Language = self.m_Language
                if not msg.get(a_Language, None):
                    a_Language = self.m_BotMessages.a_DefaultLanguage
            new_msg = msg[a_Language].get(self.m_MessageName, self)
            if a_Language == self.m_Language:
                self.m_MessageDesc = new_msg.m_MessageDesc
                self.m_Language = new_msg.m_Language
                self.m_PhotoID = new_msg.m_PhotoID
                self.m_DateTime = new_msg.m_DateTime
        return new_msg

def MakeBotMessage(a_MessageDesc):
    return BotMessage(None, '', a_MessageDesc, None, 0, None)

class BotMessages:
    def __init__(self, a_DefaultLanguage):
        self.a_DefaultLanguage = a_DefaultLanguage
        self.m_Messages = {}
        self.m_LastUpdate = None

    def GetMessages(self):
        return self.m_Messages

    def UpdateSignal(self, a_DateTime):
        self.m_LastUpdate = a_DateTime

    def CreateMessage(self, a_MessageName, a_MessageDesc, a_DateTime):
        cur_msg = BotMessage(self, a_MessageName, a_MessageDesc, self.a_DefaultLanguage, 0, a_DateTime)
        msg = self.GetMessages()
        if not msg.get(self.a_DefaultLanguage, None):
            msg[self.a_DefaultLanguage] = {}
        if not msg[self.a_DefaultLanguage].get(a_MessageName, None):
            msg[self.a_DefaultLanguage][a_MessageName] = cur_msg
        return cur_msg

