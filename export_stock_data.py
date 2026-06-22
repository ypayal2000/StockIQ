import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/stock_market_db"
)

df = pd.read_sql(
    "SELECT * FROM stock_prices",
    engine
)

df.to_csv(
    "stock_prices.csv",
    index=False
)

print(f"Exported {len(df)} rows")