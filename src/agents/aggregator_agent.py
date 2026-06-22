from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_factory import get_llm

from src.utils.logger import logger


class AggregatorAgent:

    def __init__(self):

        self.llm = get_llm()

        self.prompt = ChatPromptTemplate.from_template(
            """
You are a professional equity research analyst.

Use the information below to generate an investment recommendation.

Prediction Data:
{prediction}

News Data:
{news}

Fundamental Analysis:
{analysis}

Generate an investment recommendation.

Rules:

- Use ONLY the information provided.
- Do NOT invent target prices.
- Do NOT invent expected returns.
- Do NOT invent company names.
- If information is unavailable, do not mention it.
- Keep recommendation grounded in the provided data.

Return:

Expected Direction
Probability Up
Probability Down
Confidence Score
Risk Level
Key Growth Drivers
Key Risks
Recommendation

Keep the response concise and investor-focused.
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
