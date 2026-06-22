from src.prediction.predict import StockPredictor
from src.prediction.ai_analyst import AIAnalyst

from src.utils.logger import logger


class FinalAnalyst:

    def __init__(self):

        self.predictor = StockPredictor()
        self.analyst = AIAnalyst()


    def analyze_stock(self, symbol: str):

        logger.info(f"Analyzing {symbol}")

        # -------------------------
        # Prediction Engine
        # -------------------------

        prediction_result = (self.predictor.predict(symbol))
        prediction = (prediction_result["prediction"])

        probability_up = (prediction_result["probability_up"])
        probability_down = (prediction_result["probability_down"])
        sentiment_score = (prediction_result["sentiment_score"])

        # -------------------------
        # AI Analyst
        # -------------------------

        report = (
            self.analyst.generate_report(
                symbol=symbol,
                prediction=prediction,
                probability_up=probability_up,
                probability_down=probability_down,
                sentiment_score=sentiment_score
            )
        )

        return report


    def display_report(self, report):

        print("\n")
        print("=" * 60)

        print(f"Stock: {report['symbol']}")
        print(f"Prediction: {report['prediction']}")

        print(f"Probability Up: "f"{report['probability_up']}%")
        print(f"Probability Down: "f"{report['probability_down']}%")
        print(f"Confidence: "f"{report['confidence']}%")

        print(f"Risk Level: "f"{report['risk_level']}")
        print(f"Sentiment: "f"{report['sentiment']}")

        print("\nKey Drivers")
        print("-" * 60)

        for item in report["growth_drivers"]:
            print(f"• {item}")

        print("\nKey Risks")
        print("-" * 60)

        for item in report["risks"]:
            print(f"• {item}")

        print("\nBusiness Outlook")
        print("-" * 60)

        for item in report["outlook"]:
            print(f"• {item}")

        print("\n")
        print("=" * 60)