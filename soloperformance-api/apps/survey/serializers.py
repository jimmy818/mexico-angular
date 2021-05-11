from rest_framework import serializers, exceptions
from . import models



class QuestionSurveySerializer(serializers.ModelSerializer):
    # timezone = TimezoneField()
    class Meta:
        model = models.Question
        fields = '__all__'

class SurveySerializer(serializers.ModelSerializer):
    question_set = QuestionSurveySerializer(many=True)
    class Meta:
        model = models.Survey
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnswerText
        fields = '__all__'