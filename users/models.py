from django.db import models
from django.contrib.auth.models import AbstractUser


class GenderChoices(models.TextChoices):
    MALE = ("male", "Male")
    FEMALE = ("female", "Female")


class User(AbstractUser):
    """사용자 모델"""
    avatar = models.URLField(
        blank=True,
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices,
        default="",
    )
    class Meta:
        db_table = "user"
