from typing import List
from ..strategies.arbitrage import ArbitrageOpportunity

class RiskManager:
    def __init__(self, settings):
        self.settings = settings
        self.max_trade_amount = settings.MAX_TRADE_AMOUNT
        self.risk_level = settings.RISK_LEVEL

    def filter_opportunities(self, opportunities: List[ArbitrageOpportunity]) -> List[ArbitrageOpportunity]:
        """Filter arbitrage opportunities based on risk parameters"""
        filtered = []
        
        for opportunity in opportunities:
            if self._passes_risk_checks(opportunity):
                filtered.append(opportunity)
        
        return filtered

    def _passes_risk_checks(self, opportunity: ArbitrageOpportunity) -> bool:
        """Apply risk management checks to an opportunity"""
        # Check if profit potential exceeds minimum threshold
        if opportunity.potential_profit_percent < self.settings.MIN_PROFIT_THRESHOLD:
            return False
        
        # Check if trade size is within limits
        max_trade_value = opportunity.max_volume * opportunity.buy_price
        if max_trade_value > self.max_trade_amount:
            return False
        
        # Add more risk checks based on risk_level
        if self.risk_level == 'low':
            if opportunity.potential_profit_percent < 1.0:
                return False
        
        return True