from src.tools.market_data_tool import MarketDataTool


class MarketDataAgent:

    def __init__(self):

        self.tool = MarketDataTool()

    def run(self, state):

        symbol = state["symbol"]
        result = self.tool.get_latest_price(symbol)

        if result is None:
            state["market_data_result"] = {}
            return state

        formatted = {
            "symbol": result["symbol"],
            "trade_date": str(result["trade_date"]),
            "close_price": f"₹{result['close']:,.2f}",
            "volume": f"{result['volume']/1_000_000:.2f} Million Shares",
            "day_range": f"₹{result['low']:,.2f} - ₹{result['high']:,.2f}"
            }

        state["market_data_result"] = formatted

        return state