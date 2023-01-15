"""

"""
import yfinance as yf


def get_stock_price(ticker_symbol: str = "ADBE") -> float:
    """

    :param ticker_symbol:
    :type ticker_symbol:
    :return:
    :rtype:
    """
    stock = yf.Ticker(ticker_symbol)
    today_data = stock.history(period='1d')
    last_price = today_data['Close'][0]
    #return stock.info["regularMarketPrice"]
    return last_price


def get_stock_portfolio_value(shares: int, ticker_symbol: str) -> float:
    """

    :param shares:
    :type shares:
    :param ticker_symbol:
    :type ticker_symbol:
    :return:
    :rtype:
    """
    return shares * get_stock_price(ticker_symbol)


if __name__ == "__main__":
    print(get_stock_price())
