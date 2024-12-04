from typing import Dict, List
from dataclasses import dataclass

@dataclass
class ArbitrageOpportunity:
    buy_exchange: str
    sell_exchange: str
    symbol: str
    buy_price: float
    sell_price: float
    potential_profit_percent: float
    max_volume: float

class ArbitrageStrategy:
    def __init__(self, min_profit_threshold: float = 0.5):
        self.min_profit_threshold = min_profit_threshold

    def find_opportunities(self, prices: Dict[str, Dict]) -> List[ArbitrageOpportunity]:
        opportunities = []
        exchanges = list(prices.keys())
        
        for i, exchange1 in enumerate(exchanges):
            for exchange2 in exchanges[i+1:]:
                common_symbols = set(prices[exchange1].keys()) & set(prices[exchange2].keys())
                
                for symbol in common_symbols:
                    price1 = prices[exchange1][symbol]
                    price2 = prices[exchange2][symbol]
                    
                    if price1['bid'] > price2['ask']:
                        profit_percent = (price1['bid'] - price2['ask']) / price2['ask'] * 100
                        if profit_percent >= self.min_profit_threshold:
                            opportunities.append(self._create_opportunity(
                                exchange2, exchange1, symbol, price2['ask'],
                                price1['bid'], profit_percent,
                                min(price1['bidVolume'], price2['askVolume'])
                            ))
                    
                    elif price2['bid'] > price1['ask']:
                        profit_percent = (price2['bid'] - price1['ask']) / price1['ask'] * 100
                        if profit_percent >= self.min_profit_threshold:
                            opportunities.append(self._create_opportunity(
                                exchange1, exchange2, symbol, price1['ask'],
                                price2['bid'], profit_percent,
                                min(price2['bidVolume'], price1['askVolume'])
                            ))
        
        return sorted(opportunities, key=lambda x: x.potential_profit_percent, reverse=True)

    def _create_opportunity(self, buy_exchange, sell_exchange, symbol,
                          buy_price, sell_price, profit_percent, max_volume):
        return ArbitrageOpportunity(
            buy_exchange=buy_exchange,
            sell_exchange=sell_exchange,
            symbol=symbol,
            buy_price=buy_price,
            sell_price=sell_price,
            potential_profit_percent=profit_percent,
            max_volume=max_volume
        )