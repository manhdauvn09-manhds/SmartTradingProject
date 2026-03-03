# Abstract base class for all data providers
from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def fetch_data(self, symbol: str):
        pass
