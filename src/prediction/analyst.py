from src.prediction.predict import StockPredictor


class StockAnalyst:

    def __init__(self):

        self.predictor = StockPredictor()

    def get_sentiment_label(
        self,
        sentiment_score
    ):

        if sentiment_score >= 0.5:
            return "Very Positive"

        if sentiment_score >= 0.2:
            return "Positive"

        if sentiment_score <= -0.5:
            return "Very Negative"

        if sentiment_score <= -0.2:
            return "Negative"

        return "Neutral"

    def get_risk_level(
        self,
        confidence
    ):

        if confidence >= 0.80:
            return "Low"

        if confidence >= 0.65:
            return "Medium"

        return "High"

    def generate_drivers(
        self,
        prediction,
        sentiment_score,
        confidence
    ):

        drivers = []

        if sentiment_score <= -0.5:
            drivers.append(
                "Strong negative news sentiment"
            )

        elif sentiment_score >= 0.5:
            drivers.append(
                "Strong positive news sentiment"
            )

        if prediction == "UP":
            drivers.append(
                "Technical indicators support upside movement"
            )

        else:
            drivers.append(
                "Technical indicators indicate weakness"
            )

        if confidence > 0.60:
            drivers.append(
                "Model shows reasonable conviction"
            )

        return drivers

    def generate_risks(
        self,
        confidence,
        sentiment_score
    ):

        risks = []

        if confidence < 0.60:

            risks.append(
                "Prediction confidence is low"
            )

        if abs(sentiment_score) < 0.20:

            risks.append(
                "News sentiment is mixed"
            )

        risks.append(
            "Market conditions may change rapidly"
        )

        return risks

    def analyze(
        self,
        symbol
    ):

        prediction_data = (
            self.predictor.predict(
                symbol
            )
        )

        sentiment_label = (
            self.get_sentiment_label(
                prediction_data[
                    "sentiment_score"
                ]
            )
        )

        risk_level = (
            self.get_risk_level(
                prediction_data[
                    "confidence"
                ]
            )
        )

        drivers = (
            self.generate_drivers(
                prediction_data[
                    "prediction"
                ],
                prediction_data[
                    "sentiment_score"
                ],
                prediction_data[
                    "confidence"
                ]
            )
        )

        risks = (
            self.generate_risks(
                prediction_data[
                    "confidence"
                ],
                prediction_data[
                    "sentiment_score"
                ]
            )
        )

        return {

            "symbol":
                symbol,

            "prediction":
                prediction_data[
                    "prediction"
                ],

            "confidence":
                round(
                    prediction_data[
                        "confidence"
                    ] * 100,
                    2
                ),

            "sentiment":
                sentiment_label,

            "risk_level":
                risk_level,

            "probability_up":
                round(
                    prediction_data[
                        "probability_up"
                    ] * 100,
                    2
                ),

            "probability_down":
                round(
                    prediction_data[
                        "probability_down"
                    ] * 100,
                    2
                ),

            "key_drivers":
                drivers,

            "key_risks":
                risks
        }


if __name__ == "__main__":

    analyst = StockAnalyst()

    result = analyst.analyze(
        "TCS.NS"
    )

    print("\nStockIQ Analyst Report")
    print("=" * 50)

    print(
        f"\nStock: {result['symbol']}"
    )

    print(
        f"Prediction: {result['prediction']}"
    )

    print(
        f"Confidence: {result['confidence']}%"
    )

    print(
        f"Sentiment: {result['sentiment']}"
    )

    print(
        f"Risk Level: {result['risk_level']}"
    )

    print(
        f"Probability Up: {result['probability_up']}%"
    )

    print(
        f"Probability Down: {result['probability_down']}%"
    )

    print("\nKey Drivers:")

    for item in result["key_drivers"]:

        print(f"- {item}")

    print("\nKey Risks:")

    for item in result["key_risks"]:

        print(f"- {item}")