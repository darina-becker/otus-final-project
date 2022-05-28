from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apkstore import settings


class DevAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    dev_username = models.CharField(
        _('username'),
        max_length=50,
        unique=True,
        # help_text=_('Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.CharField(max_length=32, unique=True)
    website = models.URLField(unique=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.dev_username
