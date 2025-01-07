from abc import ABC, abstractmethod

class IQuery(ABC):
    @abstractmethod
    def buildQuery(self, parametros: dict) -> str:
        pass
    
    @abstractmethod
    def deleteNoneParams(self, parametros: dict) -> dict:
        pass