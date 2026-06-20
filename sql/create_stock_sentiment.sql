CREATE TABLE stock_sentiment (

    id SERIAL PRIMARY KEY,

    symbol VARCHAR(20),

    headline TEXT,

    source VARCHAR(100),

    published_at TIMESTAMP,

    sentiment VARCHAR(20),

    confidence FLOAT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);