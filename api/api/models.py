from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    is_admin_user = models.BooleanField(
        default=False,
        null=False,
        blank=False
    )

    is_user_administrator = models.BooleanField(
        default=False,
        null=False,
        blank=False
    )

    is_user_normal = models.BooleanField(
        default=False,
        null=False,
        blank=False
    )
