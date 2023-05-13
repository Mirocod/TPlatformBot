# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

class ModuleAgregator:
    def __init__(self):
        self.m_Modules = {}

    def GetModule(a_ModName):
        return self.m_Modules[a_ModName]

    def AddModule(a_Module):
        self.m_Modules[a_Module.GetName()] = a_Module

    def GetModList():
        self.m_Modules.items()
