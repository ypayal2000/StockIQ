import os
from dotenv import load_dotenv

from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

from src.utils.logger import logger

load_dotenv()


class PineconeRetriever:

    def __init__(self):

        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        self.pc = Pinecone(api_key=self.api_key)
        self.index = self.pc.Index(self.index_name)
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def retrieve(self, query: str, symbol: str, top_k: int = 3):

        logger.info(f"Retrieving context for {symbol}")

        query_embedding = (self.embedding_model.encode(query,
                convert_to_tensor=False).tolist())

        results = self.index.query(vector=query_embedding, top_k=top_k,
                include_metadata=True, namespace=symbol)

        documents = []

        for match in results["matches"]:
            documents.append(
                {
                    "score":round(match["score"], 4),
                    "symbol":match["metadata"]["symbol"],
                    "file_name":match["metadata"]["file_name"],
                    "document_type":match["metadata"]["document_type"],
                    "chunk_id":match["metadata"]["chunk_id"],
                    "text":match["metadata"]["text"]
                }
            )

        logger.info(f"Retrieved {len(documents)} chunks")

        return documents