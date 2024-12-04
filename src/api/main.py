from fastapi import FastAPI, HTTPException, Depends
from typing import List
from ..core.engine import ArbitrageEngine
from ..config.settings import Settings
from ..monitoring.metrics import MetricsCollector
from pydantic import BaseModel

app = FastAPI(title="Crypto Arbitrage API")
metrics_collector = MetricsCollector()

class OpportunityResponse(BaseModel):
    buy_exchange: str
    sell_exchange: str
    symbol: str
    buy_price: float
    sell_price: float
    potential_profit_percent: float
    max_volume: float

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/opportunities", response_model=List[OpportunityResponse])
async def get_opportunities(engine: ArbitrageEngine = Depends()):
    try:
        prices = await engine.fetch_all_prices()
        opportunities = engine.strategy.find_opportunities(prices)
        return opportunities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def get_metrics():
    return metrics_collector.get_metrics()

@app.post("/engine/start")
async def start_engine(engine: ArbitrageEngine = Depends()):
    try:
        await engine.start()
        return {"status": "started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/engine/stop")
async def stop_engine(engine: ArbitrageEngine = Depends()):
    try:
        await engine.stop()
        return {"status": "stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))