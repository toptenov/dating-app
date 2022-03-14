from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class Client(AbstractBaseUser):
    email = models.EmailField(_("email address"), blank=True, unique=True)
    first_name = models.CharField(blank=True, max_length=255)
    last_name = models.CharField(blank=True, max_length=255)
    is_male = models.BooleanField(blank=True)
    avatar = models.ImageField(upload_to='photos/%Y/%m/%d/', default="photos/None/No-img.jpg")

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this Client.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
        print("Email has been successfully sent")

    def __str__(self):
        return f"{self.email}"


class Match(models.Model):
    subject = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="subject_id")
    object = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="object_id")

    class Meta:
        unique_together = (('subject', 'object'), )

    def __str__(self):
        return f"{self.pk}"
