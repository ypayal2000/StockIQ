import joblib
import pandas as pd

from sqlalchemy import create_engine
from src.config.constants import FEATURE_COLUMNS

class StockPredictor:

    def __init__(self):
        self.engine = create_engine("postgresql://postgres:postgres@localhost:5432/stock_market_db")
        artifact = joblib.load("src/ml/models/stock_predictor.pkl")
        self.model = artifact["model"]
        self.features = FEATURE_COLUMNS


    def get_latest_stock_features(self, symbol: str):

        query = f"""
        SELECT *
        FROM stock_metrics
        WHERE symbol = '{symbol}'
        ORDER BY trade_date DESC
        LIMIT 1
        """

        return pd.read_sql(query, self.engine)


    def get_sentiment_score(self, symbol: str):

        query = f"""
        SELECT sentiment_score
        FROM stock_sentiment_summary
        WHERE symbol = '{symbol}'
        """

        result = pd.read_sql(query, self.engine)

        if result.empty:
            return 0.0

        return float(result.iloc[0]["sentiment_score"])


    def predict(self, symbol: str):

        stock_df = (self.get_latest_stock_features(symbol))

        if stock_df.empty:
            raise ValueError(f"No data found for {symbol}")

        X = stock_df[self.features]
        prediction = (self.model.predict(X)[0])

        probabilities = (self.model.predict_proba(X)[0])
        probability_down = round(float(probabilities[0]), 4)

        probability_up = round(float(probabilities[1]), 4)

        sentiment_score = (self.get_sentiment_score(symbol))

        confidence = round(
            max(
                probability_up,
                probability_down
            ), 4
        )

        return {
            "symbol": symbol,
            "prediction":"UP"
                if prediction == 1
                else "DOWN",
            "probability_up":probability_up,
            "probability_down":probability_down,
            "confidence":confidence,
            "sentiment_score":sentiment_score
        }


if __name__ == "__main__":

    predictor = StockPredictor()
    result = predictor.predict(
        "TCS.NS"
    )
    print("\nPrediction Result")
    print("-" * 50)
    for key, value in result.items():
        print(
            f"{key}: {value}"
        )