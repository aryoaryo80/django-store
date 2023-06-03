import boto3
from django.conf import settings


class Bucket:

    def __init__(self):
        self.conn = boto3.resource(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        self.bucket = self.conn.Bucket(settings.AWS_STORAGE_BUCKET_NAME)

    def get_bucket_objects(self):
        response = self.bucket.objects.all()
        return response

    def delete_object(self, object_name):
        self.bucket.Object(object_name).delete()

    def download_object(self, object_name):
        self.bucket.download_file(object_name, object_name.split('/')[-1])


bucket = Bucket()
