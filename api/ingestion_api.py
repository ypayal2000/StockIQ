from fastapi import FastAPI
from fastapi import BackgroundTasks
from pydantic import BaseModel

from src.ingestion.document_ingestion import DocumentIngestionPipeline


app = FastAPI()

pipeline = DocumentIngestionPipeline()


class IngestionRequest(BaseModel):

    bucket: str
    key: str


@app.post("/ingest")
def ingest_document(request: IngestionRequest, background_tasks: BackgroundTasks):

    background_tasks.add_task(pipeline.run, request.bucket, request.key)

    return {"status": "accepted"}