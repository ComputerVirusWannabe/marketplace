from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    # Collected static assets live under s3://<bucket>/static/
    location = "static"


class MediaStorage(S3Boto3Storage):
    # User uploads live under s3://<bucket>/media/
    location = "media"
    file_overwrite = False
