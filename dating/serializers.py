from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext_lazy as _

from dating.models import Client, Match


class ClientSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Client.objects.all())]
            )
    is_male = serializers.BooleanField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    avatar = serializers.ImageField(required=False, max_length=None, use_url=True)
    password = serializers.CharField(write_only=True, min_length=3)

    def create(self, validated_data):
        return Client.objects.create(**validated_data)


class MatchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='subject')
    object_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='object')

    def create(self, validated_data):
        return Match.objects.create(**validated_data)

    class Meta:
        model = Match
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('subject_id', 'object_id'),
                message=_("This match is not unique.")
            )
        ]
        fields = ('id', 'subject_id', 'object_id')
