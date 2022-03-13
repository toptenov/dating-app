from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from dating.models import Client


class ClientSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Client.objects.all())]
            )
    is_male = serializers.BooleanField()
    full_name = serializers.CharField(max_length=255)
    avatar = serializers.ImageField(required=False, max_length=None, use_url=True)
    password = serializers.CharField(write_only=True, min_length=3)
