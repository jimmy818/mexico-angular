from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from . import utils


# Create your views here.
class FilesToS3(APIView):
    def post(self, request):
        serializer = serializers.FileVideoSerializer(data=request.FILES)
        validate = serializers.ValidateFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validate.is_valid(raise_exception=True)
        if not validate.validated_data['replace']:
            print('entra')
            files = utils.validate_file_s3(serializer.validated_data['file'].name)
            if files:
                return Response(files ,status=status.HTTP_200_OK)
        files = utils.upload_file(serializer.validated_data['file'],serializer.validated_data['file'].name)

        return Response(files ,status=status.HTTP_200_OK)
