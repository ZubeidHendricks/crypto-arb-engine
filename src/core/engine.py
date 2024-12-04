import asyncio
from typing import Dict, List
from loguru import logger
from ..exchanges.base import BaseExchange
from ..strategies.arbitrage import ArbitrageStrategy
from ..risk_management.manager import RiskManager
from ..order_execution.executor import OrderExecutor

class ArbitrageEngine:
    def __init__(self, settings):
        self.settings = settings
        self.exchanges: Dict[str, BaseExchange] = {}
        self.strategy = ArbitrageStrategy()
        self.risk_manager = RiskManager(settings)
        self.order_executor = OrderExecutor(settings)
        self.is_running = False

    async def start(self):
        """Start the arbitrage engine"""
        self.is_running = True
        logger.info("Starting arbitrage engine...")
        
        try:
            await self.init_exchanges()
            await self.run_arbitrage_loop()
        except Exception as e:
            logger.error(f"Error in arbitrage engine: {e}")
            self.is_running = False
            raise

    async def init_exchanges(self):
        """Initialize exchange connections"""
        # Initialize exchange connections here
        pass

    async def run_arbitrage_loop(self):
        """Main arbitrage loop"""
        while self.is_running:
            try:
                # 1. Fetch current prices from all exchanges
                prices = await self.fetch_all_prices()
                
                # 2. Identify arbitrage opportunities
                opportunities = self.strategy.find_opportunities(prices)
                
                # 3. Filter opportunities through risk management
                valid_opportunities = self.risk_manager.filter_opportunities(opportunities)
                
                # 4. Execute valid trades
                for opportunity in valid_opportunities:
                    await self.order_executor.execute_arbitrage(opportunity)
                
                await asyncio.sleep(1)  # Avoid too frequent requests
                
            except Exception as e:
                logger.error(f"Error in arbitrage loop: {e}")
                await asyncio.sleep(5)  # Wait before retrying

    async def fetch_all_prices(self):
        """Fetch prices from all connected exchanges"""
        prices = {}
        for exchange_id, exchange in self.exchanges.items():
            try:
                prices[exchange_id] = await exchange.fetch_prices()
            except Exception as e:
                logger.error(f"Error fetching prices from {exchange_id}: {e}")
        return prices

    async def stop(self):
        """Stop the arbitrage engine"""
        self.is_running = False
        logger.info("Stopping arbitrage engine...")