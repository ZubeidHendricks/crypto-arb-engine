from abc import ABC, abstractmethod
from typing import Dict, List

class BaseExchange(ABC):
    def __init__(self, api_key: str, api_secret: str, config: Dict = None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.config = config or {}
        self.markets = {}

    @abstractmethod
    async def initialize(self):
        """Initialize exchange connection and load markets"""
        pass

    @abstractmethod
    async def fetch_prices(self, symbols: List[str] = None) -> Dict:
        """Fetch current prices for specified symbols"""
        pass

    @abstractmethod
    async def create_order(self, symbol: str, order_type: str, side: str, amount: float, price: float = None) -> Dict:
        """Create an order on the exchange"""
        pass