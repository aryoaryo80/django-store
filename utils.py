from typing import Optional
from django.contrib.auth.mixins import UserPassesTestMixin


def send_otp_code(code, phone_number):
    pass


class IsAdminMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
