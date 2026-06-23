import pandas as pd

from src.config.database import engine


class NewsTool:

    def __init__(self):

        self.engine = engine

    def get_latest_news(self, symbol, limit=5):

        query = f"""
        SELECT headline
        FROM stock_sentiment
        WHERE symbol = '{symbol}'
        ORDER BY published_at DESC
        LIMIT {limit}
        """

        return pd.read_sql(query, self.engine)


    def get_sentiment_summary(self, symbol):

        query = f"""
        SELECT *
        FROM stock_sentiment_summary
        WHERE symbol = '{symbol}'
        """

        result = pd.read_sql(query, self.engine)

        if result.empty:
            return {}

        return result.iloc[0].to_dict()