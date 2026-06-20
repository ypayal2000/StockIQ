import pandas as pd
from sqlalchemy import create_engine

from src.sentiment.news_fetcher import NewsFetcher
from src.sentiment.sentiment_analyzer import SentimentAnalyzer


class SentimentPipeline:

    def __init__(self):

        self.fetcher = NewsFetcher()

        self.analyzer = SentimentAnalyzer()

        self.engine = create_engine(
            "postgresql://postgres:postgres@localhost:5432/stock_market_db"
        )

    def fetch_news(self):

        print("Fetching news...")

        return self.fetcher.fetch_news()

    def analyze_news(self, df):

        print("Analyzing sentiment...")

        sentiments = []
        confidences = []

        for headline in df["headline"]:

            result = self.analyzer.analyze(
                headline
            )

            sentiments.append(
                result["sentiment"]
            )

            confidences.append(
                result["confidence"]
            )

        df["sentiment"] = sentiments

        df["confidence"] = confidences

        return df

    def save_to_db(self, df):

        print("Saving to PostgreSQL...")

        df = df.rename(
            columns={
                "published":
                "published_at"
            }
        )

        df.to_sql(
            "stock_sentiment",
            self.engine,
            if_exists="append",
            index=False
        )

        print(
            f"{len(df)} rows saved."
        )

    def run(self):

        news_df = self.fetch_news()

        sentiment_df = self.analyze_news(
            news_df
        )

        print("\nSample Results:")

        print(
            sentiment_df.head()
        )

        self.save_to_db(
            sentiment_df
        )

        print(
            "\nSentiment Pipeline Completed"
        )


if __name__ == "__main__":

    pipeline = SentimentPipeline()

    pipeline.run()