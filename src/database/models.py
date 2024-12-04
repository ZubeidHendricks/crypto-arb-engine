from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    buy_exchange = Column(String)
    sell_exchange = Column(String)
    buy_price = Column(Float)
    sell_price = Column(Float)
    amount = Column(Float)
    profit = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String)  # 'completed', 'failed', 'pending'

class ArbitrageOpportunity(Base):
    __tablename__ = 'arbitrage_opportunities'

    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    buy_exchange = Column(String)
    sell_exchange = Column(String)
    buy_price = Column(Float)
    sell_price = Column(Float)
    potential_profit = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    executed = Column(Boolean, default=False)

class ExchangeBalance(Base):
    __tablename__ = 'exchange_balances'

    id = Column(Integer, primary_key=True)
    exchange = Column(String)
    currency = Column(String)
    free = Column(Float)
    used = Column(Float)
    total = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)