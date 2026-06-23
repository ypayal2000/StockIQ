import boto3

from src.upload.symbol_mapper import get_folder_name


class S3Uploader:

    def __init__(self):

        self.bucket = "stockiq-documents"
        self.s3 = boto3.client("s3")


    def upload_file(self, file_path: str, file_name: str, symbol: str):

        folder = get_folder_name(symbol)
        key = f"{folder}/{file_name}"

        self.s3.upload_file(
            file_path,
            self.bucket,
            key
        )

        return key