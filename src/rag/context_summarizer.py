# from src.utils.logger import logger


# class ContextSummarizer:

#     def summarize(self, documents):

#         logger.info(f"Summarizing {len(documents)} documents")

#         combined_text = " ".join(doc["text"] for doc in documents)
#         sentences = [
#             sentence.strip()
#             for sentence in combined_text.split(".")
#             if len(sentence.strip()) > 30
#         ]

#         growth_drivers = []
#         risks = []
#         outlook = []

#         growth_keywords = [
#             "growth",
#             "opportunity",
#             "expansion",
#             "ai",
#             "cloud",
#             "digital",
#             "innovation",
#             "investment"
#         ]

#         risk_keywords = [
#             "risk",
#             "challenge",
#             "uncertainty",
#             "slowdown",
#             "competition",
#             "threat"
#         ]

#         outlook_keywords = [
#             "outlook",
#             "future",
#             "expect",
#             "strategy",
#             "vision",
#             "focus"
#         ]

#         for sentence in sentences:
#             sentence_lower = sentence.lower()
#             if any(
#                 keyword in sentence_lower
#                 for keyword in growth_keywords
#             ):
#                 growth_drivers.append(sentence)

#             if any(
#                 keyword in sentence_lower
#                 for keyword in risk_keywords
#             ):
#                 risks.append(sentence)

#             if any(
#                 keyword in sentence_lower
#                 for keyword in outlook_keywords
#             ):
#                 outlook.append(sentence)

#         return {
#             "growth_drivers":growth_drivers[:5],
#             "risks":risks[:5],
#             "outlook":outlook[:5]
#         }

import json
import re

from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_factory import get_llm
from src.utils.logger import logger


class ContextSummarizer:

    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_template(
            """
        You are a financial analyst.
        Analyze the context.

        IMPORTANT:
        Return ONLY a JSON object.
        Do NOT add explanations.
        Do NOT add markdown.
        Do NOT add ```json.
        Do NOT add notes.

        Context:{context}

        JSON format:
        {{
            "growth_drivers":["...", "..."],
            "risks":["...", "..."],
            "outlook":["...", "..."]
        }}
        """
        )


    def summarize(self, documents):

        logger.info(f"Summarizing {len(documents)} documents")

        context = "\n\n".join(doc["text"] for doc in documents)
        chain = self.prompt | self.llm

        response = chain.invoke({"context": context[:12000]})

        try:
            json_match = re.search(r"\{.*\}", response.content, re.DOTALL)

            if not json_match:
                raise ValueError("No JSON found")

            parsed_json = json.loads(json_match.group())
            return parsed_json

        except Exception as e:
            logger.warning(f"Failed to parse JSON: {e}")

            return {
                "growth_drivers": [],
                "risks": [],
                "outlook": []
            }