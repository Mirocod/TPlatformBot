# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

from abc import ABC, abstractmethod

class IModule(ABC):
    @abstractmethod
    def GetName(self):
        pass

    @abstractmethod
    def GetInitBDCommands(self):
        pass

    @abstractmethod
    def GetAccess(self):
        pass

    @abstractmethod
    def GetModuleButtons(self):
        pass

    @abstractmethod
    def RegisterHandlers(self):
        pass
