from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_factory import get_llm


class NewsSummarizer:

    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_template(
        """
        You are a professional stock market analyst.

        Analyze the following news headlines.

        News Headlines:
        {headlines}

        Sentiment Score:
        {sentiment_score}

        Generate a concise news brief.

        Rules:
        - Maximum 150 words
        - Mention key events
        - Mention market sentiment
        - Explain possible impact on stock
        - Use professional language

        Return only the summary.
        """
        )


    def summarize(self, headlines, sentiment_score):

        headline_text = "\n".join(f"- {headline}" for headline in headlines)

        chain = self.prompt | self.llm

        response = chain.invoke({"headlines": headline_text, "sentiment_score": sentiment_score})

        return response.content