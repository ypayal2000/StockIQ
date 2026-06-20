from transformers import pipeline


class SentimentAnalyzer:

    def __init__(self):

        print("Loading FinBERT model...")

        self.classifier = pipeline(
            "text-classification",
            model="ProsusAI/finbert"
        )

    def analyze(self, text):

        result = self.classifier(text)[0]

        return {
            "sentiment": result["label"],
            "confidence": round(
                result["score"],
                4
            )
        }


if __name__ == "__main__":

    analyzer = SentimentAnalyzer()

    headlines = [

        "TCS wins major cloud contract",

        "Infosys reports weak quarterly earnings",

        "Reliance announces expansion plans"
    ]

    for headline in headlines:

        result = analyzer.analyze(headline)

        print("\nHeadline:")
        print(headline)

        print(result)