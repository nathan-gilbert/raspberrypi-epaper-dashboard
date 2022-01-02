import yfinance as yf


def get_adbe():
    # define the ticker symbol
    tickerSymbol = 'ADBE'

    # get data on this ticker
    tickerData = yf.Ticker(tickerSymbol)

    print(tickerData.info["currentPrice"])


if __name__ == "__main__":
    adbe = get_adbe()
