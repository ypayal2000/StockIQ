
from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_factory import get_llm


class RouterLLM:

    def __init__(self):

        self.llm = get_llm()

        self.prompt = ChatPromptTemplate.from_template(
        """
        You are a stock assistant router.
        Classify the query into one route.

        Valid routes:
        news
        prediction
        analysis

        Return ONLY the route name.

        Query:
        {query}
        """
        )


    def route(self, query):

        chain = self.prompt | self.llm
        response = chain.invoke({"query": query})

        route = response.content.strip().lower()

        if route not in ["news", "prediction", "analysis"]:
            return "analysis"

        return route