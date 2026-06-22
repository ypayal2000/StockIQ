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


CREATE TABLE IF NOT EXISTS stock_sentiment_summary (

    symbol VARCHAR(20),

    total_articles INTEGER,

    positive_count INTEGER,

    negative_count INTEGER,

    neutral_count INTEGER,

    sentiment_score FLOAT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);