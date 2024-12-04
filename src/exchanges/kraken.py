import ccxt.async_support as ccxt
from typing import Dict, List
from .base import BaseExchange

class KrakenExchange(BaseExchange):
    def __init__(self, api_key: str, api_secret: str, config: Dict = None):
        super().__init__(api_key, api_secret, config)
        self.exchange = ccxt.kraken({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'timeout': 30000,
        })

    async def initialize(self):
        await self.exchange.load_markets()
        self.markets = self.exchange.markets
        self.pairs_mapping = self._create_pairs_mapping()

    def _create_pairs_mapping(self):
        """Create mapping for Kraken's unique pair names"""
        mapping = {}
        for market_id, market in self.markets.items():
            mapping[market['id']] = market['symbol']
        return mapping

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
                self.logger.error(f"Error fetching {symbol} from Kraken: {e}")

        return prices

    async def create_order(self, symbol: str, order_type: str, side: str, amount: float, price: float = None) -> Dict:
        try:
            return await self.exchange.create_order(symbol, order_type, side, amount, price)
        except Exception as e:
            self.logger.error(f"Error creating order on Kraken: {e}")
            raise