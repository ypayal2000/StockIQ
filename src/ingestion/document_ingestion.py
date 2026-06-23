from src.ingestion.s3_downloader import S3Downloader
from src.rag.ingestion_pipeline import RAGIngestionPipeline
from src.agents.symbol_extractor import SymbolExtractor

from src.utils.logger import logger
from src.ingestion.document_registry import DocumentRegistry


class DocumentIngestionPipeline:

    def __init__(self):

        self.downloader = S3Downloader()
        self.rag_pipeline = RAGIngestionPipeline()
        self.symbol_extractor = SymbolExtractor()
        self.registry = DocumentRegistry()


    def run(self, bucket: str, key: str):

        logger.info(f"Processing {key}")

        if self.registry.document_exists(key):
            logger.info(f"Document already processed: {key}")
            return

        local_file = self.downloader.download(bucket=bucket, key=key)
        symbol = self.symbol_extractor.extract_from_s3_key(key)
        self.rag_pipeline.ingest_document(file_path=local_file, symbol=symbol)

        logger.info(f"saving document details in table")
        self.registry.register_document(symbol=symbol, file_name=key.split("/")[-1],
            s3_key=key)

        logger.info("Document processed successfully")