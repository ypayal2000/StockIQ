from src.ingestion.s3_downloader import S3Downloader
from src.rag.ingestion_pipeline import RAGIngestionPipeline
from src.agents.symbol_extractor import SymbolExtractor

from src.utils.logger import logger


class DocumentIngestionPipeline:

    def __init__(self):

        self.downloader = S3Downloader()
        self.rag_pipeline = RAGIngestionPipeline()
        self.symbol_extractor = SymbolExtractor()


    def run(self, bucket: str, key: str):

        logger.info(f"Processing {key}")

        local_file = self.downloader.download(bucket=bucket, key=key)
        symbol = self.symbol_extractor.extract_from_s3_key(key)
        self.rag_pipeline.ingest_document(file_path=local_file, symbol=symbol)

        logger.info("Document processed successfully")