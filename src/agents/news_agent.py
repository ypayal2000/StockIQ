from src.tools.news_tool import NewsTool
from src.agents.news_summarizer import NewsSummarizer


class NewsAgent:

    def __init__(self):

        self.tool = NewsTool()
        self.summarizer = NewsSummarizer()

    def run(self, state):

        symbol = state["symbol"]
        news_df = self.tool.get_latest_news(symbol)
        summary = self.tool.get_sentiment_summary(symbol)

        headlines = (news_df["headline"].tolist())
        sentiment_score = (summary.get( "sentiment_score", 0))

        news_brief = (self.summarizer.summarize( headlines, sentiment_score))

        state["news_result"] = {
            "symbol": symbol,
            "sentiment_score": sentiment_score,
            "total_articles": summary.get("total_articles", 0),
            "summary": news_brief
        }

        return state