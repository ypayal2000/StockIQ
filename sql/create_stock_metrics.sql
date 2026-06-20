CREATE TABLE IF NOT EXISTS stock_metrics (

    symbol VARCHAR(20),

    trade_date DATE,

    close NUMERIC,

    moving_avg_3 NUMERIC,

    daily_return_pct NUMERIC,

    volatility NUMERIC,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);