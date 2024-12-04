import ccxt.async_support as ccxt
from typing import Dict, List
from .base import BaseExchange

class BinanceExchange(BaseExchange):
    def __init__(self, api_key: str, api_secret: str, config: Dict = None):
        super().__init__(api_key, api_secret, config)
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
        })

    async def initialize(self):
        await self.exchange.load_markets()
        self.markets = self.exchange.markets

    async def fetch_prices(self, symbols: List[str] = None) -> Dict:
        if symbols is None:
            symbols = list(self.markets.keys())
        
        prices = {}
        for symbol in symbols:
            ticker = await self.exchange.fetch_ticker(symbol)
            prices[symbol] = {
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'bidVolume': ticker['bidVolume'],
                'askVolume': ticker['askVolume']
            }
        return prices