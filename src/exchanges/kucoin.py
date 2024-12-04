import ccxt.async_support as ccxt
from typing import Dict, List
from .base import BaseExchange

class KucoinExchange(BaseExchange):
    def __init__(self, api_key: str, api_secret: str, passphrase: str, config: Dict = None):
        super().__init__(api_key, api_secret, config)
        self.exchange = ccxt.kucoin({
            'apiKey': api_key,
            'secret': api_secret,
            'password': passphrase,
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

    async def create_order(self, symbol: str, order_type: str, side: str, amount: float, price: float = None) -> Dict:
        return await self.exchange.create_order(symbol, order_type, side, amount, price)