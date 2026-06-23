FOLDER_SYMBOL_MAP = {
    "TCS": "TCS.NS",
    "INFY": "INFY.NS",
    "ITC": "ITC.NS",
    "RELIANCE": "RELIANCE.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "HINDUNILVR": "HINDUNILVR.NS"
}


def get_symbol(folder):

    return FOLDER_SYMBOL_MAP.get(folder, folder)