from celery import shared_task
from datetime import datetime, timedelta
from pytz import timezone
from .models import OtpCode


@shared_task
def remove_expired_otp_codes():
    expired = datetime.now(tz=timezone('Asia/Tehran')
                           ) - timedelta(seconds=120)
    OtpCode.objects.filter(created__lt=expired).delete()
