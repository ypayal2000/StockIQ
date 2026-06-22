import pandas as pd
from sqlalchemy import create_engine
from src.agents.news_summarizer import NewsSummarizer


class NewsAgent:

    def __init__(self):

        self.engine = create_engine("postgresql://postgres:postgres@localhost:5432/stock_market_db")
        self.summarizer = NewsSummarizer()


    def get_latest_news(self, symbol: str, limit: int = 5):

        query = f"""
        SELECT
            headline,
            sentiment,
            confidence,
            published_at
        FROM stock_sentiment
        WHERE symbol = '{symbol}'
        ORDER BY published_at DESC
        LIMIT {limit}
        """

        return pd.read_sql(query, self.engine)


    def get_sentiment_summary(self, symbol: str):

        query = f"""
        SELECT *
        FROM stock_sentiment_summary
        WHERE symbol = '{symbol}'
        """

        result = pd.read_sql(query, self.engine)

        if result.empty:
            return {}

        return result.iloc[0].to_dict()


    def run(self, state):

        symbol = state["symbol"]     
        news_df = self.get_latest_news(symbol)
        summary = self.get_sentiment_summary(symbol)

        headlines = (news_df["headline"].tolist())
        sentiment_score = (summary.get("sentiment_score", 0))
        news_brief = (self.summarizer.summarize(headlines, sentiment_score))

        state["news_result"] = {
            "symbol": symbol,
            "sentiment_score": sentiment_score,
            "total_articles": summary.get("total_articles", 0),
            "summary": news_brief
        }

        return state