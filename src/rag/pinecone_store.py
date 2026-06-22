import os

from pinecone import Pinecone
from pinecone import ServerlessSpec

from dotenv import load_dotenv

from src.utils.logger import logger

load_dotenv()


class PineconeStore:

    def __init__(self):

        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        self.pc = Pinecone(api_key=self.api_key)
        self._create_index_if_needed()
        self.index = self.pc.Index(self.index_name)


    def _create_index_if_needed(self):

        existing_indexes = [index["name"] for index in self.pc.list_indexes()]

        if self.index_name in existing_indexes:
            return

        logger.info(f"Creating Pinecone index: {self.index_name}")

        self.pc.create_index(
            name=self.index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )


    def store_embeddings(self, embedded_chunks, symbol):

        logger.info(f"Storing {len(embedded_chunks)} vectors")
        vectors = []

        for chunk in embedded_chunks:
            vector_id = (f"{symbol}_" f"{chunk['chunk_id']}")

            vectors.append(
                {
                    "id": vector_id,
                    "values":chunk["embedding"],
                    "metadata": {
                        "symbol":symbol,
                        "file_name":chunk["file_name"],
                        "file_path":chunk["file_path"],
                        "document_type":chunk["document_type"],
                        "chunk_id":chunk["chunk_id"],
                        "text":chunk["text"]
                    }
                }
            )

        batch_size = 100

        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            self.index.upsert(vectors=batch, namespace=symbol)
            logger.info(f"Stored batch " f"{i // batch_size + 1}")

        logger.info(f"Stored {len(vectors)} vectors")