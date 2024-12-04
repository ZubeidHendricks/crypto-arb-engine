import numpy as np
from typing import Dict, List
from dataclasses import dataclass
from ..database.models import Trade

@dataclass
class MarketMetrics:
    mean_spread: float
    volatility: float
    correlation: float
    success_rate: float

class StatisticalAnalysis:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.price_history: Dict[str, List[float]] = {}

    def update_prices(self, symbol: str, price: float):
        if symbol not in self.price_history:
            self.price_history[symbol] = []
        
        self.price_history[symbol].append(price)
        
        if len(self.price_history[symbol]) > self.window_size:
            self.price_history[symbol].pop(0)

    def calculate_metrics(self, symbol: str) -> MarketMetrics:
        if symbol not in self.price_history or len(self.price_history[symbol]) < 2:
            return None

        prices = np.array(self.price_history[symbol])
        returns = np.diff(prices) / prices[:-1]

        metrics = MarketMetrics(
            mean_spread=np.mean(np.abs(np.diff(prices))),
            volatility=np.std(returns) * np.sqrt(252),  # Annualized volatility
            correlation=self._calculate_correlation(prices),
            success_rate=self._calculate_success_rate(symbol)
        )

        return metrics

    def _calculate_correlation(self, prices: np.ndarray) -> float:
        if len(prices) < 2:
            return 0
        return np.corrcoef(prices[:-1], prices[1:])[0, 1]

    def _calculate_success_rate(self, symbol: str) -> float:
        # Calculate success rate based on historical trades
        # This would be implemented with actual trade history data
        return 0.0

    def should_trade(self, symbol: str, profit_threshold: float) -> bool:
        metrics = self.calculate_metrics(symbol)
        if not metrics:
            return False

        # Decision logic based on market metrics
        if metrics.volatility > 0.5:  # High volatility
            return False

        if metrics.correlation > 0.8:  # Strong mean reversion
            return True

        if metrics.success_rate < 0.4:  # Poor historical performance
            return False

        return True