from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import datetime, timedelta
from pytz import timezone


class Command(BaseCommand):

    def handle(self, *args, **options):
        expired = datetime.now(tz=timezone('Asia/Tehran')
                               ) - timedelta(seconds=120)
        OtpCode.objects.filter(created__lt=expired).delete()
        self.stdout.write('expired otp code detected')
