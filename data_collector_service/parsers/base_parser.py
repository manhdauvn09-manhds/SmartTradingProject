# Abstract base class for data parsers
from abc import ABC, abstractmethod
from typing import Optional
from models.stock_data import StockData

class BaseParser(ABC):
    @abstractmethod
    def parse(self, raw_data: dict) -> Optional[StockData]:
        """Parses raw data dictionary into a structured StockData model."""
        pass
