# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

from abc import ABC, abstractmethod

class IModule(ABC):
    @abstractmethod
    def GetName():
        pass

    @abstractmethod
    def GetInitBDCommands():
        pass

    @abstractmethod
    def GetAccess():
        pass

    @abstractmethod
    def GetModuleButtons():
        pass

    @abstractmethod
    def RegisterHandlers():
        pass
