from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters as df
from django_filters import rest_framework as filters
from . import models
from . import serializers
# Create your views here.

class RegionListView(viewsets.ReadOnlyModelViewSet):
    queryset = models.Region.objects.all()
    serializer_class = serializers.RegionSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('name',)
    search_fields = ('name', )
