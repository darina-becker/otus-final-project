from django.contrib.auth.models import AbstractUser
from django.db import models

from developer.models import DevAccount


class Account(AbstractUser):
    email = models.EmailField(unique=True)
    birth_date = models.DateField(blank=True, null=True)
    is_developer = models.BooleanField(default=False)

    @property
    def dev_name(self):
        try:
            result = DevAccount.objects.only('user').filter(user=self.pk).first().dev_username
        except:
            result = None

        return result
