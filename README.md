# 🚀 Crypto Trading Bot - Binance Futures Testnet

A Python-based cryptocurrency trading bot for Binance Futures Testnet with market orders, limit orders, and stop-loss functionality.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Binance](https://img.shields.io/badge/Binance-Futures%20Testnet-yellow.svg)
![Status](https://img.shields.io/badge/status-Active-brightgreen.svg)

## ✨ Features

- 🛒 **Market Orders** - Execute trades at current market price
- 📈 **Limit Orders** - Set specific buy/sell price levels  
- 🛡️ **Stop-Loss Orders** - Risk management functionality
- 📊 **Real-time Pricing** - Live cryptocurrency prices
- 💰 **Account Management** - Balance tracking and portfolio overview
- 📝 **Comprehensive Logging** - Detailed activity logs
- 🖥️ **Interactive CLI** - User-friendly command-line interface

## 🔧 Installation
Clone repository
git clone https://github.com/yourusername/crypto-trading-bot.git
cd crypto-trading-bot

Create virtual environment
python -m venv venv
venv\Scripts\activate # Windows

source venv/bin/activate # macOS/Linux
Install dependencies
pip install -r requirements.txt

Create logs directory
mkdir logs
## ⚙️ Configuration

1. Get API credentials from [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Set environment variables:
## 🚀 Usage
python main.py
### Menu Options
- View Account Info
- Get Symbol Price  
- Place Market/Limit/Stop-Loss Orders
- View/Cancel Orders
- Quick Trade Interface

## 📁 Project Structure
crypto-trading-bot/
├── main.py                    # Main application
├── bot.py                     # Trading bot implementation  
├── requirements.txt           # Dependencies
├── logs/                      # Log files
└── README.md                  # Documentation

## 📦 Dependencies

python-binance==1.0.19
pandas==2.0.3
numpy==1.24.3
colorama==0.4.6

## ⚠️ Disclaimer

- **TESTNET ONLY** - Educational purposes
- **NOT FINANCIAL ADVICE** 
- Cryptocurrency trading involves significant risk
- Test thoroughly before any real trading

.gitignore
__pycache__/
*.pyc
venv/
.env
logs/*.log
.DS_Store
*.tmp
requirements.txt
python-binance==1.0.19
pandas==2.0.3
numpy==1.24.3
colorama==0.4.6

