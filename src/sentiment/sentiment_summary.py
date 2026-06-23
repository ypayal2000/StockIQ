import pandas as pd
from src.config.database import engine


class SentimentSummary:

    def __init__(self):
        self.engine = engine


    def load_data(self):
        query = """
        SELECT
            symbol,
            sentiment
        FROM stock_sentiment
        """

        return pd.read_sql(query, self.engine)


    def create_summary(self, df):
        summary_rows = []

        for symbol in df["symbol"].unique():
            stock_df = (df[df["symbol"] == symbol])
            total = len(stock_df)

            positive = (stock_df["sentiment"].eq("positive").sum())
            negative = (stock_df["sentiment"].eq("negative").sum())
            neutral = (stock_df["sentiment"].eq("neutral").sum())

            score = (positive - negative) / total

            summary_rows.append({
                "symbol": symbol,
                "total_articles": total,
                "positive_count": positive,
                "negative_count": negative,
                "neutral_count": neutral,
                "sentiment_score": round(score, 4)})

        return pd.DataFrame(summary_rows)


    def save(self, df):
        df.to_sql("stock_sentiment_summary", self.engine, if_exists="replace", index=False)


    def run(self):

        df = self.load_data()
        summary_df = self.create_summary(df)

        print(summary_df)
        self.save(summary_df)

        print("\nSummary Created Successfully")


if __name__ == "__main__":
    SentimentSummary().run()