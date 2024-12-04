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
        self.is_running = True
        logger.info("Starting arbitrage engine...")
        
        try:
            await self.init_exchanges()
            await self.run_arbitrage_loop()
        except Exception as e:
            logger.error(f"Error in arbitrage engine: {e}")
            self.is_running = False
            raise

    async def run_arbitrage_loop(self):
        while self.is_running:
            try:
                prices = await self.fetch_all_prices()
                opportunities = self.strategy.find_opportunities(prices)
                valid_opportunities = self.risk_manager.filter_opportunities(opportunities)
                
                for opportunity in valid_opportunities:
                    await self.order_executor.execute_arbitrage(opportunity)
                
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error in arbitrage loop: {e}")
                await asyncio.sleep(5)