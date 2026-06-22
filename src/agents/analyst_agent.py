from src.prediction.final_analyst import FinalAnalyst


class AnalysisAgent:

    def __init__(self):
        self.analyst = FinalAnalyst()

    def run(self, state):
        symbol = state["symbol"]
        report = self.analyst.analyze_stock(symbol)
        state["analysis_result"] = report

        return state