# src/agents/symbol_extractor.py

class SymbolExtractor:

    SYMBOL_MAP = {
        "tcs": "TCS.NS",
        "infosys": "INFY.NS",
        "infy": "INFY.NS",
        "reliance": "RELIANCE.NS",
        "hdfc": "HDFCBANK.NS",
        "itc": "ITC.NS",
        "hul": "HINDUNILVR.NS"
    }

    def extract(self, query: str):

        query = query.lower()

        for name, symbol in self.SYMBOL_MAP.items():
            if name in query:
                return symbol

        return "TCS.NS"