from src.rag.rag_service import RAGService
from src.rag.context_summarizer import ContextSummarizer
from src.utils.logger import logger


class AIAnalyst:

    def __init__(self):
        self.rag_service = RAGService()
        self.summarizer = ContextSummarizer()


    def determine_risk_level(self, confidence):
        if confidence >= 0.80:
            return "Low"

        if confidence >= 0.60:
            return "Medium"

        return "High"


    def generate_report(self, symbol, prediction, probability_up, probability_down, sentiment_score):

        logger.info(f"Generating analyst report for {symbol}")

        rag_result = (
            self.rag_service.get_context(
                query="Growth drivers, risks and business outlook",
                symbol=symbol,
                top_k=3
            )
        )


        summary = self.summarizer.summarize(rag_result["documents"])
        confidence = max(probability_up, probability_down)

        risk_level = (self.determine_risk_level(confidence))
        sentiment = "Neutral"

        if sentiment_score > 0.25:
            sentiment = "Positive"

        elif sentiment_score < -0.25:
            sentiment = "Negative"

        report = {
            "symbol": symbol,
            "prediction": prediction,
            "probability_up":round(probability_up * 100, 2),
            "probability_down":round(probability_down * 100,2),
            "confidence":round(confidence * 100, 2),
            "risk_level":risk_level,
            "sentiment":sentiment,
            "rag_context":rag_result["context"],
            "growth_drivers": summary["growth_drivers"],
            "risks": summary["risks"],
            "outlook": summary["outlook"]
        }

        return report
    

    def display_report(self, report):

        print("\n")
        print("=" * 60)

        print(f"Stock: {report['symbol']}")
        print(f"Prediction: {report['prediction']}")

        print( f"Probability Up:"f"{report['probability_up']}%")
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