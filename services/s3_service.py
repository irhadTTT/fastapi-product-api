import boto3

BUCKET_NAME = "stockflow-files-2026"

s3 = boto3.client("s3")


def upload_file(file_content: bytes, key: str, content_type: str | None = None):
    extra_args = {}

    if content_type:
        extra_args["ContentType"] = content_type

    s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=file_content, **extra_args)


def download_file(key: str):
    response = s3.get_object(Bucket=BUCKET_NAME, Key=key)

    return response["Body"].read()


def delete_file(key: str):
    s3.delete_object(Bucket=BUCKET_NAME, Key=key)
