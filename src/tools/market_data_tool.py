import pandas as pd

from src.config.database import engine


class MarketDataTool:

    def __init__(self):

        self.engine = engine


    def get_latest_price(self, symbol):

        query = f"""
        SELECT
            symbol,
            trade_date,
            open,
            high,
            low,
            close,
            volume
        FROM stock_prices
        WHERE symbol = '{symbol}'
        ORDER BY trade_date DESC
        LIMIT 1
        """

        result = pd.read_sql(query, self.engine)

        if result.empty:
            return None

        return result.iloc[0].to_dict()