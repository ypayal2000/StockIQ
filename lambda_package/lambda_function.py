import json
import requests


FASTAPI_URL = "https://daisy-reopen-monsieur.ngrok-free.dev/ingest"


def lambda_handler(event, context):

    record = event["Records"][0]

    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    print(f"Bucket: {bucket}")
    print(f"Key: {key}")

    response = requests.post(
        FASTAPI_URL,
        json={
            "bucket": bucket,
            "key": key
        },
        timeout=10
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "bucket": bucket,
                "key": key,
                "api_response": response.json()
            }
        )
    }