import ccxt.async_support as ccxt
from typing import Dict, List
from .base import BaseExchange
from loguru import logger

class BybitExchange(BaseExchange):
    def __init__(self, api_key: str, api_secret: str, config: Dict = None):
        super().__init__(api_key, api_secret, config)
        self.exchange = ccxt.bybit({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
            }
        })

    async def initialize(self):
        await self.exchange.load_markets()
        self.markets = self.exchange.markets
        await self._init_websocket()

    async def _init_websocket(self):
        """Initialize WebSocket connection for real-time data"""
        self.ws = await self.exchange.watch_ticker_all()
        logger.info(f"Initialized WebSocket connection for Bybit")

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
                logger.error(f"Error fetching {symbol} from Bybit: {e}")

        return prices

    async def create_order(self, symbol: str, order_type: str, side: str, 
                         amount: float, price: float = None) -> Dict:
        try:
            return await self.exchange.create_order(
                symbol=symbol,
                type=order_type,
                side=side,
                amount=amount,
                price=price
            )
        except Exception as e:
            logger.error(f"Error creating order on Bybit: {e}")
            raise