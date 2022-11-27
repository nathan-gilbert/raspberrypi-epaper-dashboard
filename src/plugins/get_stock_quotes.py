import yfinance as yf


def get_stock_price(ticker_symbol: str = "ADBE") -> float:
    ticker_data = yf.Ticker(ticker_symbol)
    return ticker_data.info["currentPrice"]


if __name__ == "__main__":
    adobe_price = get_stock_price()
    print(adobe_price)
