from rest_framework import serializers, exceptions
from . import models
from apps.catalog import models as catalog_model
from apps.catalog import utils as catalog_util
from apps.teams import serializers as serializer_team
from apps.security import models as security_model

import datetime


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Widget
        fields = '__all__'


class WidgetUserSerializer(serializers.ModelSerializer):
    widget = WidgetSerializer()
    class Meta:
        model = models.UserWidget
        fields = ('widget','id','axis_x','axis_y','size',)
        
class WidgetUserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserWidget
        fields = '__all__'
    

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        exclude = ('created_at','updated_at','created_by')

class EventPosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventPoster
        exclude = ('created_at','updated_at')

class AthleteCalendarSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='full_name')
    image = serializers.ImageField(source='photo')

    class Meta:
        model = security_model.User
        fields = ('id', 'name', 'image',)

class TeamCalendarSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(read_only=True)
    start = serializers.SerializerMethodField(read_only=True)
    end = serializers.SerializerMethodField(read_only=True)
    athletes = AthleteCalendarSerializer(many=True, read_only=True)

    class Meta:
        model = catalog_model.Workout
        fields = ('id', 'name', 'date', 'start', 'end', 'athletes',)

    def get_date(self, obj):
        try:
            day = obj.day
            week = day.week
            if week and week.starts:
                year, numberWeek, weekday = catalog_util.get_year_and_week(week.starts)
                return datetime.date.fromisocalendar(year, numberWeek, day.day).strftime("%m-%d-%Y")
        except Exception as e:
            pass

        return None

    def get_start(self, obj):
        if obj.start_time:
            return {
                "hour": obj.start_time.hour,
                "minute": obj.start_time.minute,
            }
        return None

    def get_end(self, obj):
        if obj.end_time:
            return {
                "hour": obj.end_time.hour,
                "minute": obj.end_time.minute,
            }
        return None
