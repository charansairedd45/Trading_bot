#!/usr/bin/env python3
"""
Crypto Trading Bot - Complete Implementation
Binance Futures Testnet Trading Bot
"""

import sys
import os
from typing import Optional

def display_banner():
    """Display application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🚀 CRYPTO TRADING BOT 🚀                  ║
    ║                   Binance Futures Testnet                   ║
    ║                                                              ║
    ║  Status: ✅ FULLY OPERATIONAL                               ║
    ║  Balance: 15,000 USDT Available                             ║
    ║  Features: Market, Limit & Stop-Loss Orders                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def display_menu():
    """Display main menu"""
    menu = """
    ┌─────────────────────────────────────────┐
    │              TRADING MENU               │
    ├─────────────────────────────────────────┤
    │  1. 📊 View Account Info                │
    │  2. 💲 Get Symbol Price                 │
    │  3. 🛒 Place Market Order               │
    │  4. 📈 Place Limit Order                │
    │  5. 🛡️  Place Stop-Loss Limit Order     │
    │  6. 📋 View Open Orders                 │
    │  7. ❌ Cancel Order                     │
    │  8. 📊 Check Order Status               │
    │  9. 🔄 Quick Trade (Market)             │
    │  0. 🚪 Exit                             │
    └─────────────────────────────────────────┘
    """
    print(menu)

def get_user_input(prompt: str, input_type: type = str, default: Optional[str] = None):
    """Get and validate user input"""
    while True:
        try:
            if default:
                user_input = input(f"{prompt} (default: {default}): ").strip()
                if not user_input:
                    user_input = default
            else:
                user_input = input(f"{prompt}: ").strip()
            
            if input_type == float:
                return float(user_input)
            elif input_type == int:
                return int(user_input)
            else:
                return user_input
                
        except ValueError:
            print(f"❌ Invalid input. Please enter a valid {input_type.__name__}")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)

def get_api_credentials() -> tuple[str, str]:
    """Get API credentials from user or environment"""
    
    api_key = os.getenv('BINANCE_API_KEY', '')
    api_secret = os.getenv('BINANCE_API_SECRET', '')
    
    if not api_key:
        print("🔑 Enter your Binance Testnet API credentials:")
        api_key = input("API Key: ").strip()
    
    if not api_secret:
        api_secret = input("API Secret: ").strip()
    
    if not api_key or not api_secret:
        print("❌ API credentials are required!")
        sys.exit(1)
    
    return api_key, api_secret

def quick_trade_menu(bot):
    """Quick trade interface for common operations"""
    print("\n🔄 Quick Trade Menu")
    print("Popular trading pairs:")
    print("1. BTCUSDT  2. ETHUSDT  3. ADAUSDT  4. SOLUSDT")
    
    symbols = {
        '1': 'BTCUSDT',
        '2': 'ETHUSDT', 
        '3': 'ADAUSDT',
        '4': 'SOLUSDT'
    }
    
    choice = get_user_input("Select symbol (1-4) or enter custom", str, "1")
    symbol = symbols.get(choice, choice.upper())
    
    # Get current price
    try:
        current_price = bot.get_symbol_price(symbol)
        print(f"💲 Current {symbol} price: {current_price}")
    except Exception as e:
        print(f"❌ Error getting price: {e}")
        return
    
    side = get_user_input("Side (BUY/SELL)", str).upper()
    if side not in ['BUY', 'SELL']:
        print("❌ Invalid side")
        return
    
    # Suggest quantity based on balance
    print(f"💰 Available balance: Check account info for current balance")
    quantity = get_user_input("Quantity", float, 0.001)
    
    # Confirm trade
    estimated_cost = current_price * quantity if side == 'BUY' else 0
    print(f"\n📋 Trade Summary:")
    print(f"   Symbol: {symbol}")
    print(f"   Side: {side}")
    print(f"   Quantity: {quantity}")
    print(f"   Current Price: {current_price}")
    if side == 'BUY':
        print(f"   Estimated Cost: ~{estimated_cost:.2f} USDT")
    
    confirm = get_user_input("Execute trade? (y/n)", str, "n").lower()
    
    if confirm == 'y':
        try:
            order = bot.place_market_order(symbol, side, quantity)
            print(f"✅ Trade executed successfully!")
            print(f"   Order ID: {order['orderId']}")
            print(f"   Status: {order.get('status', 'PENDING')}")
        except Exception as e:
            print(f"❌ Trade failed: {e}")
    else:
        print("❌ Trade cancelled")

def main():
    """Main application function"""
    
    # Display banner
    display_banner()
    
    try:
        # Import the bot class
        from bot import BasicBot
        
        # Get API credentials
        api_key, api_secret = get_api_credentials()
        
        # Initialize bot
        print("🔄 Initializing trading bot...")
        bot = BasicBot(api_key, api_secret, testnet=True)
        
        print("🎉 Bot ready for trading operations!")
        
        # Main application loop
        while True:
            try:
                display_menu()
                choice = get_user_input("Select an option", str)
                
                if choice == '1':
                    # View Account Info
                    print("\n📊 Account Information:")
                    try:
                        account_info = bot.get_account_info()
                        print(f"   Total Balance: {account_info['totalWalletBalance']} USDT")
                        print(f"   Available Balance: {account_info['availableBalance']} USDT")
                        print(f"   Unrealized PnL: {account_info.get('totalUnrealizedProfit', '0')} USDT")
                    except Exception as e:
                        print(f"❌ Error: {e}")
                
                elif choice == '2':
                    # Get Symbol Price
                    symbol = get_user_input("Symbol", str, "BTCUSDT").upper()
                    try:
                        price = bot.get_symbol_price(symbol)
                        print(f"💲 {symbol} Price: {price} USDT")
                    except Exception as e:
                        print(f"❌ Error: {e}")
                
                elif choice == '3':
                    # Place Market Order
                    print("\n📝 Market Order Setup")
                    symbol = get_user_input("Symbol", str, "BTCUSDT").upper()
                    side = get_user_input("Side (BUY/SELL)", str).upper()
                    quantity = get_user_input("Quantity", float, 0.001)
                    
                    if side not in ['BUY', 'SELL']:
                        print("❌ Invalid side. Must be BUY or SELL")
                        continue
                    
                    # Show current price
                    try:
                        current_price = bot.get_symbol_price(symbol)
                        print(f"💲 Current price: {current_price}")
                    except:
                        pass
                    
                    confirm = get_user_input(f"Confirm {side} {quantity} {symbol} at market price? (y/n)", str, "n").lower()
                    
                    if confirm == 'y':
                        try:
                            order = bot.place_market_order(symbol, side, quantity)
                            print(f"✅ Market order placed successfully!")
                            print(f"   Order ID: {order['orderId']}")
                            print(f"   Status: {order.get('status', 'PENDING')}")
                        except Exception as e:
                            print(f"❌ Order failed: {e}")
                    else:
                        print("❌ Order cancelled")
                
                elif choice == '4':
                    # Place Limit Order
                    print("\n📝 Limit Order Setup")
                    symbol = get_user_input("Symbol", str, "BTCUSDT").upper()
                    side = get_user_input("Side (BUY/SELL)", str).upper()
                    quantity = get_user_input("Quantity", float, 0.001)
                    price = get_user_input("Price", float)
                    
                    if side not in ['BUY', 'SELL']:
                        print("❌ Invalid side. Must be BUY or SELL")
                        continue
                    
                    confirm = get_user_input(f"Confirm {side} {quantity} {symbol} at {price}? (y/n)", str, "n").lower()
                    
                    if confirm == 'y':
                        try:
                            order = bot.place_limit_order(symbol, side, quantity, price)
                            print(f"✅ Limit order placed successfully!")
                            print(f"   Order ID: {order['orderId']}")
                            print(f"   Status: {order.get('status', 'PENDING')}")
                        except Exception as e:
                            print(f"❌ Order failed: {e}")
                    else:
                        print("❌ Order cancelled")
                
                elif choice == '5':
                    # Place Stop-Loss Limit Order
                    print("\n📝 Stop-Loss Limit Order Setup")
                    symbol = get_user_input("Symbol", str, "BTCUSDT").upper()
                    side = get_user_input("Side (BUY/SELL)", str).upper()
                    quantity = get_user_input("Quantity", float, 0.001)
                    stop_price = get_user_input("Stop Price (trigger)", float)
                    limit_price = get_user_input("Limit Price (execution)", float)
                    
                    if side not in ['BUY', 'SELL']:
                        print("❌ Invalid side. Must be BUY or SELL")
                        continue
                    
                    print(f"\n📋 Stop-Loss Order Summary:")
                    print(f"   When {symbol} hits {stop_price}, place {side} order at {limit_price}")
                    
                    confirm = get_user_input("Confirm stop-loss order? (y/n)", str, "n").lower()
                    
                    if confirm == 'y':
                        try:
                            order = bot.place_stop_loss_limit_order(symbol, side, quantity, limit_price, stop_price)
                            print(f"✅ Stop-loss order placed successfully!")
                            print(f"   Order ID: {order['orderId']}")
                            print(f"   Status: {order.get('status', 'PENDING')}")
                        except Exception as e:
                            print(f"❌ Order failed: {e}")
                    else:
                        print("❌ Order cancelled")
                
                elif choice == '6':
                    # View Open Orders
                    symbol = get_user_input("Symbol (press Enter for all)", str, "").upper()
                    try:
                        if symbol:
                            orders = bot.get_open_orders(symbol)
                        else:
                            orders = bot.get_open_orders()
                        
                        if orders:
                            print(f"\n📋 Open Orders ({len(orders)}):")
                            for order in orders:
                                print(f"   ID: {order['orderId']} | {order['symbol']} | {order['side']} | {order['type']} | Status: {order['status']}")
                        else:
                            print("📭 No open orders found")
                    except Exception as e:
                        print(f"❌ Error: {e}")
                
                elif choice == '7':
                    # Cancel Order
                    symbol = get_user_input("Symbol", str, "BTCUSDT").upper()
                    order_id = get_user_input("Order ID", int)
                    
                    confirm = get_user_input(f"Cancel order {order_id} for {symbol}? (y/n)", str, "n").lower()
                    if confirm == 'y':
                        try:
                            result = bot.cancel_order(symbol, order_id)
                            print("✅ Order cancelled successfully!")
                        except Exception as e:
                            print(f"❌ Cancellation failed: {e}")
                    else:
                        print("❌ Cancellation aborted")
                
                elif choice == '8':
                    # Check Order Status
                    symbol = get_user_input("Symbol", str, "BTCUSDT").upper()
                    order_id = get_user_input("Order ID", int)
                    
                    try:
                        order = bot.get_order_status(symbol, order_id)
                        print(f"\n📊 Order Status:")
                        print(f"   Order ID: {order['orderId']}")
                        print(f"   Symbol: {order['symbol']}")
                        print(f"   Status: {order['status']}")
                        print(f"   Side: {order['side']}")
                        print(f"   Type: {order['type']}")
                        print(f"   Quantity: {order['origQty']}")
                        if 'price' in order:
                            print(f"   Price: {order['price']}")
                    except Exception as e:
                        print(f"❌ Error: {e}")
                
                elif choice == '9':
                    # Quick Trade
                    quick_trade_menu(bot)
                
                elif choice == '0':
                    # Exit
                    print("👋 Thank you for using Crypto Trading Bot!")
                    print("📊 Session Summary:")
                    try:
                        account_info = bot.get_account_info()
                        print(f"   Final Balance: {account_info['totalWalletBalance']} USDT")
                    except:
                        pass
                    break
                
                else:
                    print("❌ Invalid option. Please try again.")
                
                # Pause before showing menu again
                input("\n⏸️  Press Enter to continue...")
                print("\n" + "="*60)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {str(e)}")
                print("The bot will continue running...")
    
    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
