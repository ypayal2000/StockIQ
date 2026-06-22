from src.rag.document_loader import DocumentLoader
from src.rag.chunker import DocumentChunker
from src.rag.embedder import EmbeddingGenerator
from src.rag.pinecone_store import PineconeStore

from src.utils.logger import logger


class RAGIngestionPipeline:

    def __init__(self):

        self.loader = DocumentLoader()
        self.chunker = DocumentChunker(chunk_size=1000, chunk_overlap=200)
        self.embedder = EmbeddingGenerator()
        self.vector_store = PineconeStore()


    def ingest_document(self, file_path: str, symbol: str):

        logger.info(f"Starting ingestion for {file_path}")

        document = self.loader.load_document(file_path)
        chunks = self.chunker.chunk_document(document)
        
        embedded_chunks = (self.embedder.embed_chunks(chunks))
        self.vector_store.store_embeddings(embedded_chunks,symbol)

        logger.info(f"Ingestion completed for {file_path}")


    def ingest_documents(self, documents: list):

        for document in documents:
            self.ingest_document(
                file_path=document["file_path"],
                symbol=document["symbol"]
            )