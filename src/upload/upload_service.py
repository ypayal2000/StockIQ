from pathlib import Path

from src.upload.s3_uploader import S3Uploader


class UploadService:

    def __init__(self):

        self.uploader = S3Uploader()


    def upload_document(self, uploaded_file, symbol):

        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)

        file_path = temp_dir / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        key = self.uploader.upload_file(
            file_path=str(file_path),
            file_name=uploaded_file.name,
            symbol=symbol
        )

        return key