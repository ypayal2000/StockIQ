SYMBOL_FOLDER_MAP = {
    "TCS.NS": "TCS",
    "INFY.NS": "INFY",
    "ITC.NS": "ITC",
    "RELIANCE.NS": "RELIANCE",
    "HDFCBANK.NS": "HDFCBANK",
    "HINDUNILVR.NS": "HINDUNILVR"
}


def get_folder_name(symbol: str):

    return SYMBOL_FOLDER_MAP.get(
        symbol,
        symbol.replace(".NS", "")
    )