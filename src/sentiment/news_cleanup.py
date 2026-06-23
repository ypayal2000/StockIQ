from sqlalchemy import create_engine
from sqlalchemy import text

from src.utils.logger import logger
from src.config.database import engine

class NewsCleanup:

    def __init__(self):

        self.engine = engine

    def run(self):

        query = """
        DELETE FROM stock_sentiment
        WHERE published_at <
        CURRENT_DATE - INTERVAL '10 days'
        """

        with self.engine.begin() as conn:
            result = conn.execute(text(query))

        logger.info(f"Deleted {result.rowcount} old news articles")


if __name__ == "__main__":

    NewsCleanup().run()