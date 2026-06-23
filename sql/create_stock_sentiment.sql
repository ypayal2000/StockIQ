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


CREATE TABLE document_registry (

    id SERIAL PRIMARY KEY,

    symbol VARCHAR(50),

    file_name VARCHAR(500),

    s3_key VARCHAR(1000),

    upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    status VARCHAR(50)
);