from typing import TypedDict, Optional


class StockState(TypedDict):

    user_query: str
    symbol: Optional[str]
    agents: Optional[list]

    news_result: Optional[dict]
    prediction_result: Optional[dict]
    analysis_result: Optional[dict]
    market_data_result: Optional[dict]

    response: Optional[dict]