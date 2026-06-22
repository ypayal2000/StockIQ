from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.utils.logger import logger


class DocumentChunker:

    def __init__(self, chunk_size=1000, chunk_overlap=200):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )

    def chunk_document(self, document):

        logger.info(f"Creating chunks for {document['file_name']}")

        chunks = self.splitter.split_text(document["content"])
        chunk_documents = []

        for idx, chunk in enumerate(chunks):
            chunk_documents.append(
                {
                    "file_name": document["file_name"],
                    "file_path": document["file_path"],
                    "document_type": document["document_type"],
                    "chunk_id": idx,
                    "text": chunk
                }
            )

        logger.info(f"Created {len(chunk_documents)} chunks")
        return chunk_documents