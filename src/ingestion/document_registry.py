import pandas as pd

from sqlalchemy import create_engine
from src.utils.logger import logger
from src.config.database import engine

class DocumentRegistry:

    def __init__(self):

        self.engine = engine


    def document_exists(self, s3_key):

        query = f"""
        SELECT *
        FROM document_registry
        WHERE s3_key = '{s3_key}'
        """
        
        result = pd.read_sql(query, self.engine)

        return not result.empty


    def register_document(self, symbol, file_name, s3_key, status="completed"):

        logger.info("Registering document")
        df = pd.DataFrame(
            [
                {
                    "symbol": symbol,
                    "file_name": file_name,
                    "s3_key": s3_key,
                    "status": status
                }
            ]
        )

        df.to_sql(
            "document_registry",
            self.engine,
            if_exists="append",
            index=False
        )

        logger.info("Document registered successfully")