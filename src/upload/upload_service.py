from pathlib import Path

from src.upload.s3_uploader import S3Uploader
from src.ingestion.document_registry import DocumentRegistry
from src.upload.symbol_mapper import get_folder_name

class UploadService:

    def __init__(self):

        self.uploader = S3Uploader()
        self.registry = DocumentRegistry()


    def upload_document(self, uploaded_file, symbol):

        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)

        file_path = temp_dir / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        folder = get_folder_name(symbol)
        key = f"{folder}/{uploaded_file.name}"

        if self.registry.document_exists(key):
            return {"status": "exists", "key": key}

        key = self.uploader.upload_file(
            file_path=str(file_path),
            file_name=uploaded_file.name,
            symbol=symbol
        )

        return {"status": "uploaded", "key": key}