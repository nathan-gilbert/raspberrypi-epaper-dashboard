import yfinance as yf


def get_stock_price(ticker_symbol: str = "ADBE") -> float:
    ticker_data = yf.Ticker(ticker_symbol)
    return ticker_data.info["currentPrice"]
