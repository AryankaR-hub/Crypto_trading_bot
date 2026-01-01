import time
from binance.client import Client
from requests.exceptions import ReadTimeout, ConnectionError
from config import API_KEY, API_SECRET
from logger import logger


class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        # Increase timeout to avoid frequent failures
        self.client = Client(api_key, api_secret, {"timeout": 20})

        if testnet:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com"

        logger.info("BasicBot initialized")

    #  RETRY HANDLER 

    def retry_request(self, func, retries=3, delay=3):
        for attempt in range(1, retries + 1):
            try:
                return func()
            except (ReadTimeout, ConnectionError) as e:
                print(f"⏳ Network issue... retrying ({attempt}/{retries})")
                logger.warning(f"Network error attempt {attempt}: {e}")
                time.sleep(delay)
            except Exception as e:
                raise e
        raise Exception("❌ Request failed after multiple retries")

    #  CONNECTION TEST 

    def test_connection(self):
        try:
            self.retry_request(lambda: self.client.futures_ping())
            print("✅ Connected to Binance Futures Testnet")
            logger.info("Connection successful")
        except Exception as e:
            print("❌ Connection failed:", e)
            logger.error(f"Connection failed: {e}")

    #  BALANCE 

    def get_usdt_balance(self):
        try:
            balances = self.retry_request(
                lambda: self.client.futures_account_balance()
            )
            for asset in balances:
                if asset["asset"] == "USDT":
                    balance = float(
                        asset.get("availableBalance", asset.get("balance", 0))
                    )
                    print(f"💰 USDT Balance: {balance}")
                    logger.info(f"USDT Balance: {balance}")
                    return balance

            print("⚠️ USDT balance not found")
            logger.warning("USDT balance not found")
            return 0

        except Exception as e:
            print("❌ Error fetching balance:", e)
            logger.error(f"Balance fetch failed: {e}")
            return 0

    #  LEVERAGE 

    def set_leverage(self, symbol, leverage):
        try:
            response = self.retry_request(
                lambda: self.client.futures_change_leverage(
                    symbol=symbol,
                    leverage=leverage
                )
            )
            print(f"⚙️ Leverage set to {leverage}x for {symbol}")
            logger.info(f"Leverage set: {response}")
        except Exception as e:
            print("❌ Error setting leverage:", e)
            logger.error(f"Leverage error: {e}")

    # MARKET ORDER 

    def place_market_order(self, symbol, side, quantity):
        try:
            order = self.retry_request(
                lambda: self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type="MARKET",
                    quantity=quantity
                )
            )
            print("✅ Market order executed")
            print(order)
            logger.info(f"Market order: {order}")
        except Exception as e:
            print("❌ Market order failed:", e)
            logger.error(f"Market order failed: {e}")

    #  LIMIT ORDER 

    def place_limit_order(self, symbol, side, quantity, price):
        try:
            order = self.retry_request(
                lambda: self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type="LIMIT",
                    quantity=quantity,
                    price=price,
                    timeInForce="GTC"
                )
            )
            print("✅ Limit order placed")
            print(order)
            logger.info(f"Limit order: {order}")
        except Exception as e:
            print("❌ Limit order failed:", e)
            logger.error(f"Limit order failed: {e}")


#  MAIN (CLI) 

if __name__ == "__main__":
    bot = BasicBot(API_KEY, API_SECRET, testnet=True)

    print("\n--- Binance Futures Testnet Trading Bot ---\n")

    bot.test_connection()

    symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()

    side = input("Enter side (BUY/SELL): ").upper()
    if side not in ["BUY", "SELL"]:
        print("❌ Invalid side")
        exit()

    order_type = input("Enter order type (MARKET/LIMIT): ").upper()
    if order_type not in ["MARKET", "LIMIT"]:
        print("❌ Invalid order type")
        exit()

    try:
        quantity = float(input("Enter quantity: "))
        if quantity <= 0:
            raise ValueError
    except ValueError:
        print("❌ Quantity must be a positive number")
        exit()

    try:
        leverage = int(input("Enter leverage (e.g., 5, 10): "))
        if leverage <= 0:
            raise ValueError
    except ValueError:
        print("❌ Invalid leverage")
        exit()

    bot.set_leverage(symbol, leverage)

    if order_type == "MARKET":
        bot.place_market_order(symbol, side, quantity)

    else:
        try:
            price = float(input("Enter limit price: "))
            if price <= 0:
                raise ValueError
        except ValueError:
            print("❌ Invalid price")
            exit()

        bot.place_limit_order(symbol, side, quantity, price)

    print("\n📄 Order process completed.")
