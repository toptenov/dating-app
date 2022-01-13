from django.db import models


class Participant(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64, unique=True)
    is_male = models.BooleanField()
    photo = models.ImageField(upload_to="photos/%Y/%m/%d")
