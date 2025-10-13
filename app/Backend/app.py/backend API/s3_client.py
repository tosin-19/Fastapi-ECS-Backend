import boto3
from botocore.exceptions import ClientError
from .config import get_settings

settings = get_settings()

_session = boto3.session.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)
s3 = _session.client("s3")

def upload_fileobj(fileobj, bucket, key, content_type=None):
    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type
    s3.upload_fileobj(fileobj, bucket, key, ExtraArgs=extra_args)

def generate_presigned_url(bucket, key, expires_in=None):
    expires = expires_in or settings.PRESIGNED_URL_EXPIRES
    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expires
        )
    except ClientError as e:
        raise
    return url
