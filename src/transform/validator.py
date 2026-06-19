import pandas as pd


class DataValidator:

    @staticmethod
    def validate(df: pd.DataFrame):

        if df.empty:
            raise ValueError("No data fetched")

        df.drop_duplicates(inplace=True)

        required_cols = ["Date", "Open", "High", "Low", "Close", "Volume", "symbol"]

        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")

        return df