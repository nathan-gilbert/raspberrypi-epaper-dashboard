import stockquotes


def get_adbe():
    adobe = stockquotes.Stock('ADBE')
    return adobe


if __name__ == "__main__":
    adbe = get_adbe()
    print(adbe.price)