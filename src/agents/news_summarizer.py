from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_factory import get_llm


class NewsSummarizer:

    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_template(
        """
        You are a financial news analyst.

        Summarize the headlines.

        Rules:

        - Maximum 120 words
        - Focus only on recent events
        - Mention overall sentiment
        - Do NOT provide investment advice
        - Do NOT recommend buying or selling

        Return markdown.
        """
        )


    def summarize(self, headlines, sentiment_score):

        headline_text = "\n".join(f"- {headline}" for headline in headlines)

        chain = self.prompt | self.llm

        response = chain.invoke({"headlines": headline_text, "sentiment_score": sentiment_score})

        return response.content