from rest_framework import serializers, exceptions
from . import models


class SubsciptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subscription
        exclude = ('institution',)


class SubsciptionValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subscription
        fields = '__all__'
