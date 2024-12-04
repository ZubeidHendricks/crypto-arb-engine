import ccxt.async_support as ccxt
from typing import Dict, List
from .base import BaseExchange

class FTXExchange(BaseExchange):
    def __init__(self, api_key: str, api_secret: str, subaccount: str = None, config: Dict = None):
        super().__init__(api_key, api_secret, config)
        self.exchange = ccxt.ftx({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'headers': {
                'FTX-SUBACCOUNT': subaccount
            } if subaccount else {}
        })

    async def initialize(self):
        await self.exchange.load_markets()
        self.markets = self.exchange.markets
        await self._initialize_websocket()

    async def _initialize_websocket(self):
        """Initialize websocket connection for real-time data"""
        # Implement websocket connection for better price updates
        pass

    async def fetch_prices(self, symbols: List[str] = None) -> Dict:
        if symbols is None:
            symbols = list(self.markets.keys())

        prices = {}
        for symbol in symbols:
            try:
                ticker = await self.exchange.fetch_ticker(symbol)
                prices[symbol] = {
                    'bid': ticker['bid'],
                    'ask': ticker['ask'],
                    'bidVolume': ticker.get('bidVolume', 0),
                    'askVolume': ticker.get('askVolume', 0),
                    'last': ticker['last'],
                    'timestamp': ticker['timestamp']
                }
            except Exception as e:
                self.logger.error(f"Error fetching {symbol} from FTX: {e}")

        return prices