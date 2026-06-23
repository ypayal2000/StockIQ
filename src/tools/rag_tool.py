from src.rag.rag_service import RAGService


class RAGTool:

    def __init__(self):

        self.rag = RAGService()

    def get_context(self, query, symbol, top_k=5):

        return self.rag.get_context(
            query=query,
            symbol=symbol,
            top_k=top_k
        )