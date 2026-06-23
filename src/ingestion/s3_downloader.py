import os
import boto3

from src.utils.logger import logger


class S3Downloader:

    def __init__(self):

        self.s3 = boto3.client("s3")

    def download(self, bucket: str, key: str):

        os.makedirs("temp", exist_ok=True)
        file_name = os.path.basename(key)
        local_path = os.path.join("temp", file_name)

        logger.info(f"Downloading {key} from {bucket}")

        self.s3.download_file(bucket, key, local_path)

        logger.info(f"Downloaded to {local_path}")

        return local_path