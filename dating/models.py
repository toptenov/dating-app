from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(AbstractBaseUser):
    email = models.EmailField(_("email address"), blank=True, unique=True)
    first_name = models.CharField(blank=True, max_length=255)
    last_name = models.CharField(blank=True, max_length=255)
    is_male = models.BooleanField(blank=True)
    avatar = models.ImageField(upload_to='photos/%Y/%m/%d/', default="photos/None/No-img.jpg")

    USERNAME_FIELD = "email"

    def __str__(self):
        return f"{self.email}"
