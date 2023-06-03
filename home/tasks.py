from celery import shared_task
from bucket import bucket


def get_bucket_objects():
    return bucket.get_bucket_objects()


@shared_task
def delete_object(object):
    return bucket.delete_object(object)


@shared_task
def download_object(object):
    return bucket.download_object(object)
