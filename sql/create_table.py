"""Script to create a table"""
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="stock_market_db",
    user="postgres",
    password="postgres"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS stock_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    trade_date DATE,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()

print("Table Created")

cursor.close()
conn.close()