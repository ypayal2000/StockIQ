from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_factory import get_llm


class NewsSummarizer:

    def __init__(self):

        self.llm = get_llm()

        self.prompt = ChatPromptTemplate.from_template(
        """
        You are a financial news analyst.

        Summarize ONLY the provided headlines.

        Rules:

        - Use ONLY the headlines provided below
        - Do NOT invent news events
        - Do NOT mention companies not present in headlines
        - Maximum 120 words
        - Mention overall sentiment
        - Do NOT provide investment advice
        - Do NOT recommend buying or selling

        Headlines:
        {headlines}

        Sentiment Score:
        {sentiment_score}

        Return markdown.
        """
        )


    def summarize(self, headlines, sentiment_score):

        headline_text = "\n".join(f"- {headline}" for headline in headlines)

        chain = self.prompt | self.llm

        response = chain.invoke({"headlines": headline_text, "sentiment_score": sentiment_score})

        return response.content