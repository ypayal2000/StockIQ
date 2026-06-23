from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_factory import get_llm

from src.utils.logger import logger


class AggregatorAgent:

    def __init__(self):

        self.llm = get_llm()

        self.prompt = ChatPromptTemplate.from_template(
           """
        You are a professional equity research analyst.

        Use ONLY the provided information.

        Do NOT invent:
        - target prices
        - expected returns
        - company names
        - financial metrics not provided

        Return your answer in EXACT markdown format:

        ## Investment Recommendation

        ### Expected Direction
        <value>

        ### Probability Up
        <value>

        ### Probability Down
        <value>

        ### Confidence Score
        <value>

        ### Risk Level
        <value>

        ### Key Growth Drivers
        - item 1
        - item 2

        ### Key Risks
        - item 1
        - item 2

        ### Recommendation
        <short recommendation>

        Prediction Data:
        {prediction}

        News Data:
        {news}

        Analysis Data:
        {analysis}
        """
        )

    def run(self, state):

        logger.info("Generating final investment recommendation")

        prediction_result = (state.get("prediction_result", {}))
        news_result = (state.get("news_result", {}))
        analysis_result = (state.get("analysis_result", {}))

        analysis_summary = {"prediction": analysis_result.get("prediction"),
                    "risk_level": analysis_result.get("risk_level"),
                    "sentiment": analysis_result.get("sentiment"),
                    "growth_drivers": analysis_result.get("growth_drivers"),
                    "risks": analysis_result.get("risks"),
                    "outlook": analysis_result.get("outlook")
                    }

        chain = self.prompt | self.llm

        response = chain.invoke(
            {
                "prediction": prediction_result,
                "news": news_result,
                "analysis": analysis_summary
            }
        )

        state["response"] = {
            "symbol": state["symbol"],
            "recommendation": response.content
        }

        return state
