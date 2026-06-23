from src.agents.news_agent import NewsAgent
from src.agents.prediction_agent import PredictionAgent
from src.agents.analyst_agent import AnalysisAgent
from src.agents.market_data_agent import MarketDataAgent


class ExecutorAgent:

    def __init__(self):

        self.news_agent = NewsAgent()
        self.prediction_agent = PredictionAgent()
        self.analysis_agent = AnalysisAgent()
        self.market_data_agent = MarketDataAgent()

    def run(self, state):

        agents = state.get("agents", [])

        if "prediction" in agents:
            state = self.prediction_agent.run(state)

        if "news" in agents:
            state = self.news_agent.run(state)

        if "analysis" in agents:
            state = self.analysis_agent.run(state)

        if "market_data" in agents:
            state = self.market_data_agent.run(state)

        return state