import pytest
from src.strategies.arbitrage import ArbitrageStrategy, ArbitrageOpportunity

@pytest.fixture
def strategy():
    return ArbitrageStrategy(min_profit_threshold=0.5)

@pytest.fixture
def mock_prices():
    return {
        'binance': {
            'BTC/USDT': {'bid': 50000, 'ask': 50100, 'bidVolume': 1.0, 'askVolume': 1.0},
            'ETH/USDT': {'bid': 3000, 'ask': 3010, 'bidVolume': 10.0, 'askVolume': 10.0}
        },
        'kucoin': {
            'BTC/USDT': {'bid': 50200, 'ask': 50300, 'bidVolume': 1.0, 'askVolume': 1.0},
            'ETH/USDT': {'bid': 2990, 'ask': 3000, 'bidVolume': 10.0, 'askVolume': 10.0}
        }
    }

def test_find_opportunities(strategy, mock_prices):
    opportunities = strategy.find_opportunities(mock_prices)
    
    assert len(opportunities) > 0
    
    # Test that opportunities are sorted by profit
    profits = [op.potential_profit_percent for op in opportunities]
    assert profits == sorted(profits, reverse=True)

def test_min_profit_threshold(strategy, mock_prices):
    opportunities = strategy.find_opportunities(mock_prices)
    
    for op in opportunities:
        assert op.potential_profit_percent >= strategy.min_profit_threshold