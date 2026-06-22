from src.prediction.predict import StockPredictor


class PredictionAgent:

    def __init__(self):
        self.predictor = StockPredictor()

    def run(self, state):
        symbol = state["symbol"]
        result = self.predictor.predict(symbol) 
        state["prediction_result"] = result
        return state