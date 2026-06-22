from src.rag.retriever import PineconeRetriever

from src.utils.logger import logger


class RAGService:

    def __init__(self):
        self.retriever = PineconeRetriever()


    def get_context(self, query: str, symbol: str, top_k: int = 3):

        logger.info(f"Getting context for {symbol}")

        documents = self.retriever.retrieve(query=query, symbol=symbol, top_k=top_k)
        context_parts = []

        for doc in documents:
            context_parts.append(doc["text"])

        context = "\n\n".join(context_parts)
        logger.info(f"Retrieved {len(documents)} documents")

        return {
            "query": query,
            "symbol": symbol,
            "context": context,
            "documents": documents
        }