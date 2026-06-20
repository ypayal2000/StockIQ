import pandas as pd
from src.utils.logger import logger

class PostgresLoader:

    def __init__(self, engine):
        self.engine = engine

    def load(self, df):

        df = df.rename(columns={"Date": "trade_date", "Open": "open", "High": "high",
                                "Low": "low", "Close": "close", "Volume": "volume"})

        final_df = df[[ "symbol", "trade_date", "open", "high", "low",
                    "close", "volume"]]

        # Read existing records
        existing_df = pd.read_sql(
            """
            SELECT symbol, trade_date
            FROM stock_prices
            """,
            self.engine
        )

        final_df["trade_date"] = pd.to_datetime(
            final_df["trade_date"]
        )

        existing_df["trade_date"] = pd.to_datetime(
            existing_df["trade_date"]
        )

        # Merge to identify new rows
        merged_df = final_df.merge(
            existing_df,
            on=["symbol", "trade_date"],
            how="left",
            indicator=True
        )

        new_records = merged_df[
            merged_df["_merge"] == "left_only"
        ]

        new_records = new_records[
            [
                "symbol",
                "trade_date",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]
        ]

        if new_records.empty:
            logger.info("No new records found")
            return

        new_records.to_sql(
            "stock_prices",
            self.engine,
            if_exists="append",
            index=False
        )

        logger.info(
            f"{len(new_records)} new rows inserted"
        )