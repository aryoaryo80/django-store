from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password, email=None, full_name=None):
        if phone_number and password:
            user = self.model(phone_number=phone_number,
                              email=email, full_name=full_name)
            user.set_password(password)
            user.save(using=self._db)
            return user

        raise ValueError('not complete')

    def create_superuser(self, phone_number, email, full_name, password):
        user = self.model(phone_number=phone_number,
                          email=email, full_name=full_name)
        user.set_password(password)
        user.is_admin = user.is_superuser = True
        user.save(using=self._db)
        return user
