import pandas as pd
from sqlalchemy import create_engine

from src.sentiment.news_fetcher import NewsFetcher
from src.sentiment.sentiment_analyzer import SentimentAnalyzer
from src.sentiment.sentiment_summary import SentimentSummary
from src.sentiment.news_cleanup import NewsCleanup
from src.utils.logger import logger
from src.config.database import engine


class SentimentPipeline:

    def __init__(self):

        self.fetcher = NewsFetcher()
        self.analyzer = SentimentAnalyzer()
        self.summary = SentimentSummary()
        self.cleanup = NewsCleanup()
        self.engine = engine


    def fetch_news(self):

        logger.info("Fetching news...")
        return self.fetcher.fetch_news()


    def analyze_news(self, df):

        logger.info("Analyzing sentiment...")

        sentiments = []
        confidences = []

        for headline in df["headline"]:

            result = self.analyzer.analyze(headline)
            sentiments.append(result["sentiment"])
            confidences.append(result["confidence"])

        df["sentiment"] = sentiments
        df["confidence"] = confidences

        return df


    def save_to_db(self, df):

        logger.info("Saving to PostgreSQL...")

        df = df.rename(columns={"published": "published_at"})

        # -------------------------
        # Load existing headlines
        # -------------------------

        existing_df = pd.read_sql(
            """
            SELECT headline
            FROM stock_sentiment
            """,
            self.engine
        )

        existing_headlines = set(existing_df["headline"])

        # -------------------------
        # Remove duplicates
        # -------------------------

        df = df[~df["headline"].isin(existing_headlines)]

        if df.empty:
            logger.info("No new headlines found.")
            return

        # -------------------------
        # Save new headlines
        # -------------------------

        df.to_sql("stock_sentiment", self.engine, if_exists="append", index=False)
        logger.info(f"{len(df)} new rows saved.")


    def run(self):

        news_df = self.fetch_news()
        sentiment_df = self.analyze_news(news_df)
        logger.debug("\nSample Results:")

        logger.debug(sentiment_df.head())
        self.save_to_db(sentiment_df)

        logger.info("\nCleaning old news...")
        self.cleanup.run()

        logger.info("\nUpdating sentiment summary...")
        self.summary.run()

        logger.info("\nNews Pipeline Completed")


if __name__ == "__main__":

    pipeline = SentimentPipeline()

    pipeline.run()