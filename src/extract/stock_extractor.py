import yfinance as yf
import pandas as pd
from utils.logger import logger


class StockExtractor:

    def __init__(self):
        self.tickers = ["TCS.NS", "INFY.NS", "RELIANCE.NS", "HDFCBANK.NS"]

    def extract(self):
        all_data = []

        for ticker in self.tickers:
            logger.info(f"Fetching {ticker}")
            df = yf.download(ticker, period="5d", progress=False, auto_adjust=False)

            if df.empty:
                continue

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            df.reset_index(inplace=True)

            df["symbol"] = ticker

            df = df[["Date", "Open", "High", "Low", "Close", "Volume", "symbol"]]

            all_data.append(df)

        final_df = pd.concat(all_data, ignore_index=True)

        return final_df