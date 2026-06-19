from config.database import engine

from extract.stock_extractor import StockExtractor
from transform.validator import DataValidator
from load.postgre_loader import PostgresLoader
from utils.logger import logger

def run_pipeline():

    extractor = StockExtractor()

    logger.info("Extracting stock data...")
    raw_df = extractor.extract()
    
    logger.info("Validating data...")
    validated_df = DataValidator.validate(raw_df)

    logger.info("Loading into PostgreSQL...")
    loader = PostgresLoader(engine)

    loader.load(validated_df)

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()