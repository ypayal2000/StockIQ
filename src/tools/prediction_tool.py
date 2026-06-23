from src.prediction.predict import StockPredictor


class PredictionTool:

    def __init__(self):

        self.predictor = StockPredictor()

    def predict(self, symbol):

        return self.predictor.predict(symbol)