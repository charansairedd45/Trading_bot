import os
from typing import Dict, Any

class Config:
    """Configuration class for the trading bot"""
    
    # API Configuration
    API_KEY = os.getenv('BINANCE_API_KEY', '')
    API_SECRET = os.getenv('BINANCE_API_SECRET', '')
    
    # Testnet Configuration
    TESTNET = True
    BASE_URL = 'https://testnet.binancefuture.com'
    
    # Trading Configuration
    DEFAULT_SYMBOL = 'BTCUSDT'
    DEFAULT_QUANTITY = 0.001
    
    # Logging Configuration
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/trading_bot.log'
    
    # Order Configuration
    SUPPORTED_ORDER_TYPES = ['MARKET', 'LIMIT', 'STOP_LOSS_LIMIT', 'OCO']
    SUPPORTED_SIDES = ['BUY', 'SELL']
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        if not cls.API_KEY or not cls.API_SECRET:
            print("❌ Error: API_KEY and API_SECRET must be set")
            return False
        return True
