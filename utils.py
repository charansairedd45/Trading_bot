import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def setup_logging(log_file: str = 'logs/trading_bot.log', log_level: str = 'INFO') -> logging.Logger:
    """Setup logging configuration"""
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('TradingBot')
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def print_colored(message: str, color: str = 'WHITE') -> None:
    """Print colored message to console"""
    color_map = {
        'RED': Fore.RED,
        'GREEN': Fore.GREEN,
        'YELLOW': Fore.YELLOW,
        'BLUE': Fore.BLUE,
        'MAGENTA': Fore.MAGENTA,
        'CYAN': Fore.CYAN,
        'WHITE': Fore.WHITE
    }
    print(f"{color_map.get(color.upper(), Fore.WHITE)}{message}{Style.RESET_ALL}")

def format_order_response(order: Dict[str, Any]) -> str:
    """Format order response for display"""
    return f"""
📊 Order Details:
   Order ID: {order.get('orderId', 'N/A')}
   Symbol: {order.get('symbol', 'N/A')}
   Side: {order.get('side', 'N/A')}
   Type: {order.get('type', 'N/A')}
   Quantity: {order.get('origQty', 'N/A')}
   Price: {order.get('price', 'N/A')}
   Status: {order.get('status', 'N/A')}
   Time: {datetime.fromtimestamp(order.get('transactTime', 0) / 1000)}
    """

def validate_order_params(symbol: str, side: str, order_type: str, quantity: float, 
                         price: Optional[float] = None) -> tuple[bool, str]:
    """Validate order parameters"""
    
    if not symbol or len(symbol) < 3:
        return False, "Invalid symbol"
    
    if side.upper() not in ['BUY', 'SELL']:
        return False, "Side must be BUY or SELL"
    
    if order_type.upper() not in ['MARKET', 'LIMIT', 'STOP_LOSS_LIMIT']:
        return False, "Unsupported order type"
    
    if quantity <= 0:
        return False, "Quantity must be greater than 0"
    
    if order_type.upper() in ['LIMIT', 'STOP_LOSS_LIMIT'] and (not price or price <= 0):
        return False, "Price must be specified and greater than 0 for limit orders"
    
    return True, "Valid parameters"
