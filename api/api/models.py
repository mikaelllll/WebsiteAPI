from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import FileExtensionValidator

def user_file_directory_path(instance, filename):
    return 'website/files/user_{0}/{1}'.format(instance.user.id, filename)

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

    username = models.CharField(
        max_length=256,
        null=False,
        blank=False,
        unique = True
    )

    telephone = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    cpf = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    curriculum = models.FileField(
        upload_to=user_file_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        null = True,
        blank = True
    )

    deleteDate = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True
    )

class JobVacancy(models.Model):

    userADMID = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null = True,
        blank = False
    )

    company = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    description = models.CharField(
        max_length=4000,
        null=False,
        blank=False
    )

    salary = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    createDate = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False
    )

    deleteDate = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True
    )

    isDeleted = models.BooleanField(
        default=False,
        null=False,
        blank=False
    )

    objects = models.Manager()