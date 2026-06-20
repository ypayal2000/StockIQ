import os
import pandas as pd
from sqlalchemy import create_engine


class FeatureEngineer:

    def __init__(self):

        self.engine = create_engine(
            "postgresql://postgres:postgres@localhost:5432/stock_market_db"
        )

    def load_data(self):

        query = """
                SELECT
            symbol,
            trade_date,

            close,

            moving_avg_3,
            moving_avg_5,
            moving_avg_10,
            moving_avg_20,

            daily_return_pct,
            return_3d,
            return_5d,

            avg_volume_5,
            avg_volume_20,

            price_vs_ma20,
            daily_range_pct,

            volatility,
            momentum_10,
            volume_spike,
            "rsi_14"

        FROM stock_metrics
        ORDER BY symbol, trade_date"""

        return pd.read_sql(query, self.engine)

    def create_target(self, df):

        # next day's close price
        df["next_close"] = (
            df.groupby("symbol")["close"]
            .shift(-1)
        )

        # classification target
        df["target"] = (
            df["next_close"] > df["close"]
        ).astype(int)

        return df

    def clean_data(self, df):

        df = df.drop(columns=["next_close"])

        df = df.dropna()

        return df

    def save_dataset(self, df):

        os.makedirs("data", exist_ok=True)

        output_path = "data/ml_dataset.csv"

        df.to_csv(
            output_path,
            index=False
        )

        print(f"\nDataset saved to: {output_path}")
        print(f"Total Rows: {len(df)}")

    def run(self):

        print("Loading stock metrics...")

        df = self.load_data()

        print("Creating target column...")

        df = self.create_target(df)

        print("Cleaning dataset...")

        df = self.clean_data(df)

        print("\nTarget Distribution:")
        print(df["target"].value_counts())

        self.save_dataset(df)

        print("\nFeature Engineering Completed Successfully")


if __name__ == "__main__":

    engineer = FeatureEngineer()

    engineer.run()