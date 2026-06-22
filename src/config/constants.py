DATABASE_URL = (
    "postgresql://postgres:postgres@localhost:5432/stock_market_db"
)

MODEL_PATH = (
    "src/ml/models/stock_predictor.pkl"
)

FEATURE_COLUMNS = [

    "close",

    "moving_avg_3",
    "moving_avg_5",
    "moving_avg_10",
    "moving_avg_20",

    "daily_return_pct",
    "return_3d",
    "return_5d",

    "avg_volume_5",
    "avg_volume_20",

    "price_vs_ma20",
    "daily_range_pct",

    "volatility",
    "momentum_10",
    "volume_spike",
    "rsi_14"
]

TRACKED_SYMBOLS = [

    "TCS.NS",
    "INFY.NS",
    "RELIANCE.NS",
    "HDFCBANK.NS"
]