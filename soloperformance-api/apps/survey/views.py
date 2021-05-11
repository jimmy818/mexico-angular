from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters as df
from django_filters import rest_framework as filters
from rest_framework import exceptions, status
from django.utils.translation import ugettext as _

from . import models
from . import serializers
from . import mixins
# Create your views here.

class SurveyListView(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = models.Survey.objects.all()
    serializer_class = serializers.SurveySerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('survey_type',)
    
    def get_queryset(self):
        workout = self.request.GET.get('workout')
        if workout:
            answers = models.AnswerText.objects.filter(
                workout_id=int(workout),
                user=self.request.user
            )
            if len(answers) != 0:
                return models.Survey.objects.none()
            return super().get_queryset()
        raise exceptions.ValidationError(_('workout is not valid'))




class AnswerTextView(mixins.CreateAnswerListMixin, viewsets.ModelViewSet):
    queryset = models.AnswerText.objects.all()
    serializer_class = serializers.AnswerSerializer
    

    

    