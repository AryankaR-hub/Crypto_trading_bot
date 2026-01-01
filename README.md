# Binance Futures Testnet Trading Bot

A simplified Python trading bot built using the official 
Binance Futures Testnet API.

# Features
- Connects to Binance Futures Testnet (USDT-M)
- Places MARKET and LIMIT orders
- Supports BUY and SELL sides
- Sets leverage for futures trading
- Command-line interface (CLI) for user input
- Proper logging of API requests, responses, and errors
- Handles network timeouts and API errors gracefully

# Tech Stack
- Python
- python-binance
- Binance Futures Testnet

# Setup Instructions

1.  Clone the repository
```bash
git clone <your-repo-url>
cd trading_bot

2.  Create and activate virtual environment
        python -m venv venv
        source venv/bin/activate  # Windows: venv\Scripts\activate
3.  Install dependencies
        pip install -r requirements.txt
4. Create .env file
        API_KEY=your_testnet_api_key
        API_SECRET=your_testnet_api_secret
5. Run the bot
        python bot.py


Note:
    This bot uses Binance Futures Testnet (no real money involved)



