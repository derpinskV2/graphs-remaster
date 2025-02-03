import boto3
from django.conf import settings


class S3PresignedURLMixin:
    @staticmethod
    def get_presigned_url_for_file(file_obj, user) -> str:
        if file_obj.user != user:
            raise PermissionError("You are not allowed to access this file.")

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        key = f"media/{file_obj.file.name}"
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                "Key": key,
            },
            ExpiresIn=600,
        )
        return presigned_url
