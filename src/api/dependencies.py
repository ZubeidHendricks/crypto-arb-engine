from fastapi import Depends
from ..core.engine import ArbitrageEngine
from ..config.settings import Settings

def get_settings():
    return Settings()

def get_engine(settings: Settings = Depends(get_settings)):
    return ArbitrageEngine(settings)