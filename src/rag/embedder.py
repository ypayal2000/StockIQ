from sentence_transformers import SentenceTransformer

from src.utils.logger import logger


class EmbeddingGenerator:

    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


    def embed_text(self, text: str):
        return self.model.encode(text, convert_to_tensor=False).tolist()


    def embed_chunks(self, chunks):

        logger.info(f"Generating embeddings for {len(chunks)} chunks")

        embedded_chunks = []

        for chunk in chunks:
            embedded_chunks.append(
                {
                    "file_name": chunk["file_name"],
                    "file_path": chunk["file_path"],
                    "document_type": chunk["document_type"],
                    "chunk_id": chunk["chunk_id"],
                    "text": chunk["text"],
                    "embedding": self.embed_text(chunk["text"])
                }
            )

        logger.info(f"Generated embeddings for {len(embedded_chunks)} chunks")

        return embedded_chunks