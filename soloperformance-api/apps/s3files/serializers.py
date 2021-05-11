from rest_framework import serializers

class FileVideoSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)


class ValidateFileSerializer(serializers.Serializer):
    replace = serializers.BooleanField(required=True)