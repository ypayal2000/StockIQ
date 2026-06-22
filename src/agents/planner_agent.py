import json
import re
from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_factory import get_llm


class PlannerAgent:

    def __init__(self):

        self.llm = get_llm()

        self.prompt = ChatPromptTemplate.from_template(
        """
        You are a stock intelligence planner.

        Available agents:

        news
        prediction
        analysis

        Task:

        Choose the required agents.

        Rules:

        News queries:
        → news

        Prediction queries:
        → prediction

        Analysis queries:
        → analysis

        Investment queries:
        → prediction,news,analysis

        Return ONLY valid JSON.

        Examples:

        Query:
        What is latest Infosys news?

        Output:
        {{"agents":["news"]}}

        Query:
        Predict Reliance stock

        Output:
        {{"agents":["prediction"]}}

        Query:
        What are the risks in TCS annual report?

        Output:
        {{"agents":["analysis"]}}

        Query:
        Should I buy Infosys?

        Output:
        {{"agents":["prediction","news","analysis"]}}

        User Query:
        {query}
        """
        )


    def plan(self, query):

        chain = self.prompt | self.llm
        response = chain.invoke({"query": query})

        try:
            content = response.content

            # Extract JSON block
            match = re.search( r'\{.*\}', content, re.DOTALL)
            if not match:
                raise ValueError("No JSON found")

            json_text = match.group()
            result = json.loads(json_text)

            return result["agents"]

        except Exception as e:
            print(f"Planner Parse Error: {e}")
            return ["analysis"]