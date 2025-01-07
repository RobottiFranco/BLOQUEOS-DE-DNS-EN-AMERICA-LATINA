from abc import ABC, abstractmethod

class IExecute(ABC):
    @abstractmethod
    def execute(self, url: str):
        pass
    
    @abstractmethod
    def backoff(self, attempt) -> int:
        pass