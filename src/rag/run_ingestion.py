from src.rag.ingestion_pipeline import RAGIngestionPipeline

documents = [
    {
        "symbol": "TCS.NS",
        "file_path":"data\\documents\\annual-report-2025-26.pdf"
    },
    {
        "symbol": "INFY.NS",
        "file_path":"data\\documents\\infosys-ar-26.pdf"
    }
]

pipeline = RAGIngestionPipeline()

pipeline.ingest_documents(documents)