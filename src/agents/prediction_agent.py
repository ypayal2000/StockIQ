from src.tools.prediction_tool import PredictionTool


class PredictionAgent:

    def __init__(self):

        self.tool = PredictionTool()

    def run(self, state):

        symbol = state["symbol"]
        result = self.tool.predict(symbol)
        state["prediction_result"] = (result)

        return state