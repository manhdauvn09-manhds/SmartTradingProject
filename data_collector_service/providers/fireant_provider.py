# Implementation for Fireant API
from .base_provider import BaseProvider

class FireantProvider(BaseProvider):
    def fetch_data(self, symbol: str):
        print(f"Fetching data for {symbol} from Fireant")
        return {}
