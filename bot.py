import time
import logging
from typing import Dict, Any, Optional, List
from binance import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

class BasicBot:
    """Enhanced Trading Bot for Binance Futures Testnet"""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """Initialize the trading bot"""
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Initialize Binance client
        try:
            self.client = Client(
                api_key=api_key,
                api_secret=api_secret,
                testnet=testnet
            )
            
            # Test connection
            self._test_connection()
            
            self.logger.info("Bot initialized successfully")
            print("✅ Bot initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize bot: {str(e)}")
            print(f"❌ Failed to initialize bot: {str(e)}")
            raise
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration with proper encoding"""
        import os
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Create logger
        logger = logging.getLogger('TradingBot')
        logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Create formatters (without emojis for file logging)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        
        # File handler with UTF-8 encoding
        try:
            file_handler = logging.FileHandler('logs/trading_bot.log', encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not setup file logging: {e}")
        
        # Console handler (simplified to avoid encoding issues)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _test_connection(self) -> None:
        """Test API connection"""
        try:
            account_info = self.client.futures_account()
            self.logger.info("API connection successful")
            print("🔗 API connection successful")
        except Exception as e:
            self.logger.error(f"API connection failed: {str(e)}")
            raise Exception(f"API connection failed: {str(e)}")
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information"""
        try:
            self.logger.info("Fetching account information...")
            account_info = self.client.futures_account()
            
            # Log account balance
            total_balance = float(account_info['totalWalletBalance'])
            available_balance = float(account_info['availableBalance'])
            
            self.logger.info(f"Total Balance: {total_balance} USDT")
            self.logger.info(f"Available Balance: {available_balance} USDT")
            
            return account_info
            
        except BinanceAPIException as e:
            self.logger.error(f"API Error getting account info: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error getting account info: {e}")
            raise
    
    def get_symbol_price(self, symbol: str) -> float:
        """Get current price for a symbol"""
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            self.logger.info(f"Current price for {symbol}: {price}")
            return price
        except Exception as e:
            self.logger.error(f"Error getting price for {symbol}: {e}")
            raise
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        """Place a market order"""
        
        # Validate parameters
        if not self._validate_order_params(symbol, side, 'MARKET', quantity):
            raise ValueError("Invalid order parameters")
        
        try:
            self.logger.info(f"Placing MARKET {side} order: {quantity} {symbol}")
            
            # Place actual order
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            
            self.logger.info(f"Market order placed successfully: {order['orderId']}")
            
            return order
            
        except BinanceAPIException as e:
            self.logger.error(f"Binance API Error: {e}")
            raise
        except BinanceOrderException as e:
            self.logger.error(f"Binance Order Error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error placing market order: {e}")
            raise
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict[str, Any]:
        """Place a limit order"""
        
        # Validate parameters
        if not self._validate_order_params(symbol, side, 'LIMIT', quantity, price):
            raise ValueError("Invalid order parameters")
        
        try:
            self.logger.info(f"Placing LIMIT {side} order: {quantity} {symbol} at {price}")
            
            # Place actual order
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price
            )
            
            self.logger.info(f"Limit order placed successfully: {order['orderId']}")
            
            return order
            
        except BinanceAPIException as e:
            self.logger.error(f"Binance API Error: {e}")
            raise
        except BinanceOrderException as e:
            self.logger.error(f"Binance Order Error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error placing limit order: {e}")
            raise
    
    def place_stop_loss_limit_order(self, symbol: str, side: str, quantity: float, 
                                   price: float, stop_price: float) -> Dict[str, Any]:
        """Place a stop-loss limit order"""
        
        try:
            self.logger.info(f"Placing STOP_LOSS_LIMIT {side} order: {quantity} {symbol}")
            self.logger.info(f"Stop Price: {stop_price}, Limit Price: {price}")
            
            # Place actual order
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type=ORDER_TYPE_STOP,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price,
                stopPrice=stop_price
            )
            
            self.logger.info(f"Stop-loss limit order placed successfully: {order['orderId']}")
            
            return order
            
        except BinanceAPIException as e:
            self.logger.error(f"Binance API Error: {e}")
            raise
        except BinanceOrderException as e:
            self.logger.error(f"Binance Order Error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error placing stop-loss limit order: {e}")
            raise
    
    def get_open_orders(self, symbol: str = None) -> List[Dict[str, Any]]:
        """Get open orders"""
        try:
            if symbol:
                orders = self.client.futures_get_open_orders(symbol=symbol)
                self.logger.info(f"Retrieved {len(orders)} open orders for {symbol}")
            else:
                orders = self.client.futures_get_open_orders()
                self.logger.info(f"Retrieved {len(orders)} open orders")
            
            return orders
            
        except Exception as e:
            self.logger.error(f"Error getting open orders: {e}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """Cancel an order"""
        try:
            self.logger.info(f"Cancelling order {order_id} for {symbol}")
            
            result = self.client.futures_cancel_order(
                symbol=symbol,
                orderId=order_id
            )
            
            self.logger.info(f"Order {order_id} cancelled successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Error cancelling order {order_id}: {e}")
            raise
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """Get order status"""
        try:
            order = self.client.futures_get_order(
                symbol=symbol,
                orderId=order_id
            )
            
            self.logger.info(f"Order {order_id} status: {order['status']}")
            return order
            
        except Exception as e:
            self.logger.error(f"Error getting order status: {e}")
            raise
    
    def _validate_order_params(self, symbol: str, side: str, order_type: str, quantity: float, 
                              price: Optional[float] = None) -> bool:
        """Validate order parameters"""
        
        if not symbol or len(symbol) < 3:
            self.logger.error("Invalid symbol")
            return False
        
        if side.upper() not in ['BUY', 'SELL']:
            self.logger.error("Side must be BUY or SELL")
            return False
        
        if order_type.upper() not in ['MARKET', 'LIMIT', 'STOP_LOSS_LIMIT']:
            self.logger.error("Unsupported order type")
            return False
        
        if quantity <= 0:
            self.logger.error("Quantity must be greater than 0")
            return False
        
        if order_type.upper() in ['LIMIT', 'STOP_LOSS_LIMIT'] and (not price or price <= 0):
            self.logger.error("Price must be specified and greater than 0 for limit orders")
            return False
        
        return True
