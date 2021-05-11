from rest_framework import serializers, exceptions
from . import models


# class TimezoneField(serializers.Field):
#     "Take the timezone object and make it JSON serializable"
#     def to_representation(self, obj):
#         return obj.zone

#     def to_internal_value(self, data):
#         return data

class RegionSerializer(serializers.ModelSerializer):
    # timezone = TimezoneField()
    class Meta:
        model = models.Region
        fields = '__all__'