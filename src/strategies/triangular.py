from typing import Dict, List, Tuple
from dataclasses import dataclass
from decimal import Decimal
from ..exchanges.base import BaseExchange

@dataclass
class TriangularOpportunity:
    exchange: str
    pair1: str
    pair2: str
    pair3: str
    step1_action: str  # buy/sell
    step2_action: str
    step3_action: str
    initial_amount: float
    final_amount: float
    profit_percent: float
    path: List[str]

class TriangularArbitrage:
    def __init__(self, min_profit_threshold: float = 0.5):
        self.min_profit_threshold = min_profit_threshold

    def find_opportunities(self, exchange: str, prices: Dict[str, Dict]) -> List[TriangularOpportunity]:
        opportunities = []
        pairs = list(prices.keys())
        
        # Find all possible triangular paths
        for base_pair in pairs:
            paths = self._find_triangular_paths(base_pair, pairs)
            for path in paths:
                opportunity = self._calculate_profit(exchange, path, prices)
                if opportunity and opportunity.profit_percent >= self.min_profit_threshold:
                    opportunities.append(opportunity)

        return sorted(opportunities, key=lambda x: x.profit_percent, reverse=True)

    def _find_triangular_paths(self, start_pair: str, pairs: List[str]) -> List[List[str]]:
        paths = []
        visited = set()

        def dfs(current_pair: str, path: List[str]):
            if len(path) == 3:
                # Check if the path forms a triangle
                if self._is_valid_triangle(path):
                    paths.append(path.copy())
                return

            base, quote = current_pair.split('/')
            for pair in pairs:
                if pair in visited:
                    continue

                pair_base, pair_quote = pair.split('/')
                if base in [pair_base, pair_quote] or quote in [pair_base, pair_quote]:
                    visited.add(pair)
                    path.append(pair)
                    dfs(pair, path)
                    path.pop()
                    visited.remove(pair)

        visited.add(start_pair)
        dfs(start_pair, [start_pair])
        return paths

    def _is_valid_triangle(self, path: List[str]) -> bool:
        if len(path) != 3:
            return False

        # Extract all currencies in the path
        currencies = set()
        for pair in path:
            base, quote = pair.split('/')
            currencies.add(base)
            currencies.add(quote)

        # A valid triangle should have exactly 3 currencies
        return len(currencies) == 3

    def _calculate_profit(self, exchange: str, path: List[str], prices: Dict[str, Dict]) -> TriangularOpportunity:
        try:
            initial_amount = 1.0  # Start with 1 unit of base currency
            current_amount = Decimal(str(initial_amount))
            steps = []

            for i, pair in enumerate(path):
                price_data = prices[pair]
                base, quote = pair.split('/')
                
                # Determine if we should buy or sell
                if i < len(path) - 1:
                    next_base, next_quote = path[i + 1].split('/')
                    if quote in [next_base, next_quote]:
                        # We need the quote currency, so buy
                        current_amount *= Decimal(str(price_data['ask']))
                        steps.append('buy')
                    else:
                        # We need the base currency, so sell
                        current_amount /= Decimal(str(price_data['bid']))
                        steps.append('sell')
                else:
                    # Last step - close the triangle
                    first_base, first_quote = path[0].split('/')
                    if base == first_base:
                        current_amount *= Decimal(str(price_data['ask']))
                        steps.append('buy')
                    else:
                        current_amount /= Decimal(str(price_data['bid']))
                        steps.append('sell')

            final_amount = float(current_amount)
            profit_percent = ((final_amount - initial_amount) / initial_amount) * 100

            return TriangularOpportunity(
                exchange=exchange,
                pair1=path[0],
                pair2=path[1],
                pair3=path[2],
                step1_action=steps[0],
                step2_action=steps[1],
                step3_action=steps[2],
                initial_amount=initial_amount,
                final_amount=final_amount,
                profit_percent=profit_percent,
                path=path
            )

        except (KeyError, ZeroDivisionError) as e:
            return None