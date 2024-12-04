from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class TradingMetrics:
    total_profit: float
    total_trades: int
    successful_trades: int
    failed_trades: int
    average_profit_per_trade: float
    win_rate: float

class MetricsCollector:
    def __init__(self):
        self.start_time = datetime.utcnow()
        self.trades: List[Dict] = []

    def add_trade(self, trade: Dict):
        self.trades.append({
            **trade,
            'timestamp': datetime.utcnow()
        })

    def get_metrics(self) -> TradingMetrics:
        if not self.trades:
            return TradingMetrics(
                total_profit=0,
                total_trades=0,
                successful_trades=0,
                failed_trades=0,
                average_profit_per_trade=0,
                win_rate=0
            )

        successful = [t for t in self.trades if t['status'] == 'completed']
        failed = [t for t in self.trades if t['status'] == 'failed']

        total_profit = sum(t['profit'] for t in successful)
        total_trades = len(self.trades)
        successful_trades = len(successful)
        failed_trades = len(failed)

        return TradingMetrics(
            total_profit=total_profit,
            total_trades=total_trades,
            successful_trades=successful_trades,
            failed_trades=failed_trades,
            average_profit_per_trade=total_profit / total_trades if total_trades > 0 else 0,
            win_rate=successful_trades / total_trades if total_trades > 0 else 0
        )