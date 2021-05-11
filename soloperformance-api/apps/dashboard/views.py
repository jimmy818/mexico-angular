from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from django.db.models import Q
from django.db import transaction

from rest_framework import exceptions
from rest_framework import viewsets
from rest_framework import filters as df
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView

from django_filters import rest_framework as filters

from . import models
from . import serializers
from . import utils

from apps.catalog import models as catalog_model, serializers as catalog_serializer, utils as catalog_util
from apps.teams import models as team_model, serializers as serializer_team
from apps.security import models as security_model

from datetime import date, timedelta, datetime

# Create your views here.


class WidgetView(viewsets.ReadOnlyModelViewSet):
    queryset = models.Widget.objects.all()
    serializer_class = serializers.WidgetSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    search_fields = ('name', )


class EventView(viewsets.ModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    search_fields = ('name', )
    
    def perform_create(self, serializer):
        item = serializer.save(
            created_by = self.request.user,
        )
        return item
    
    def perform_update(self, serializer):
        item = serializer.save(
            created_by = self.request.user
        )
        return item

class EventPosterView(viewsets.ModelViewSet):
    queryset = models.EventPoster.objects.all().order_by('date_start')
    serializer_class = serializers.EventPosterSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    search_fields = ('name',)
    filterset_fields = ('team','athletes')
    


class EventFilterView(APIView):
    def get(self, request):
        type = self.request.GET.get('type')
        institution = self.request.GET.get('institution')
        team = self.request.GET.get('team')
        athlete = self.request.GET.get('athlete')
        if int(type) == 1:
            # filter in days
            start = self.request.GET.get('starts')
            ends = self.request.GET.get('ends')
            start = datetime.strptime(start, '%Y-%m-%d')
            ends = datetime.strptime(ends, '%Y-%m-%d')
            range_days = [] 
            for day in utils.get_dates_range(start,ends):
                current_day = day.strftime("%Y-%m-%d")
                event = models.Event.objects.filter(
                    date_start__lte=current_day, 
                    date_end__gte=current_day,
                    created_by__institution=int(institution))
                if team:
                    event = event.filter(team=int(team))
                if athlete:
                    # teams = team_model.Team.objects.filter(institution=int(institution)).values_list('pk',flat=True)
                    # print(teams)
                    event = event.filter(athletes=int(athlete))
                event_name = event.distinct().values_list('name').first()
                event = event.distinct().count()
                event_day = {
                    "date" : current_day,
                    "events" : event ,
                    "list_event": event_name                   
                }
                range_days.append(event_day)
            return Response(range_days,status=status.HTTP_200_OK)
        elif int(type) == 2:
            #filter in years
            year = self.request.GET.get('year')
            months = []
            for _ in (number + 1 for number in range(12)):
                event = models.Event.objects.filter(
                    date_start__year=year,
                    date_end__year=year,
                    date_start__month__lte=_,
                    date_end__month__gte=_,
                    created_by__institution=int(institution))
                if team:
                    event = event.filter(team=int(team))
                if athlete:
                    # teams = team_model.Team.objects.filter(institution=int(institution)).values_list('pk',flat=True)
                    # print(teams)
                    event = event.filter(athletes=int(athlete))
                event_name = event.distinct().values_list('name',flat=True).first()
                event = event.distinct().count()
                event_day = {
                    "date" : utils.get_text_month(year,_),
                    "events" : event ,
                    "list_event": event_name                         
                }
                months.append(event_day)
            return Response(months,status=status.HTTP_200_OK)
        return Response(dict(type=type),status=status.HTTP_200_OK)

class EventListView(APIView):
    def get(self, request):
        type = self.request.GET.get('type')
        institution = self.request.GET.get('institution')
        date = self.request.GET.get('date')
        date = datetime.strptime(date, '%Y-%m-%d')
        team = self.request.GET.get('team')
        athlete = self.request.GET.get('athlete')
        if int(type) == 1:
            events = models.Event.objects.filter(
                    date_start__lte=date, 
                    date_end__gte=date,
                    created_by__institution=int(institution))
            if team:
                events = events.filter(team=int(team))
            if athlete:
                # teams = team_model.Team.objects.filter(institution=int(institution)).values_list('pk',flat=True)
                # print(teams)
                events = events.filter(athletes=int(athlete))
            events = events.distinct()
            serializer = serializers.EventSerializer(events, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif int(type) == 2:
            events = models.Event.objects.filter(
                    date_start__year=date.year,
                    date_end__year=date.year,
                    date_start__month__lte=date.month,
                    date_end__month__gte=date.month,
                    created_by__institution=int(institution))
            if team:
                events = events.filter(team=int(team))
            if athlete:
                # teams = team_model.Team.objects.filter(institution=int(institution)).values_list('pk',flat=True)
                # print(teams)
                events = events.filter(athletes=int(athlete))
            events = events.distinct()
            serializer = serializers.EventSerializer(events, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(dict(type=type),status=status.HTTP_200_OK)

class CustomWidgetView(viewsets.ModelViewSet):
    queryset = models.Widget.objects.all()
    serializer_class = serializers.WidgetUserPostSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('user', )
    
    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update',):
            return serializers.WidgetUserPostSerializer
        if self.action in ('list', 'retrieve',):
            return serializers.WidgetUserSerializer
    
    def get_queryset(self):
        user = self.request.user
        widgets = models.UserWidget.objects.filter(user=user)
        if len(widgets) == 0 and not user.deleted_widget:
            custom_widget = models.Widget.objects.filter(name__icontains='main').first()
            print(custom_widget)
            widget_user = models.UserWidget.objects.create(
                user=user,
                widget=custom_widget,
                axis_x=0,
                axis_y=0
                )
            widget_user.save()
            return [widget_user]
        else:
            return widgets
        
    def perform_create(self, serializer):
        user = self.request.user
        item = serializer.save(
            user=user
        )
        return item
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = serializers.WidgetUserSerializer(instance)
        return Response(instance_serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'size' in request.data:
            if not instance.widget.resizable:
                raise exceptions.ValidationError(_('Current widget is not resizable.'))

        serializer = serializers.WidgetUserPostSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance_serializer = serializers.WidgetUserSerializer(instance)
        return Response(instance_serializer.data)
    
    def perform_update(self, serializer):
        # pk = self.kwargs.get('pk')
        # order = self.request.data.get('order')
        # instance_updated = get_object_or_404(models.UserWidget,pk=pk)
        # if order:
        #     itemorder = models.UserWidget.objects.filter(~Q(pk=pk),order=order).first()
        #     if itemorder:
        #         itemorder.order=instance_updated.order
        #         itemorder.save()    
        return super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        user = self.request.user
        user.deleted_widget = True
        user.save()
        return super().perform_destroy(instance)
    

class CalendarListView(APIView):
    def get(self, request):
        user = request.user
        institution = user.institution

        params = request.GET
        date = params.get('date', None)
        teams = params.get('teams', [])
        athletes = params.get('athletes', [])

        if ',' in teams:
            teams = teams.split(',')
        else:
            teams = [teams] if teams else teams
        if ',' in athletes:
            athletes = athletes.split(',')
        else:
            athletes = [athletes] if athletes else athletes

        if not date:
           raise exceptions.ValidationError(_('A date is required.'))

        date = datetime.strptime(date, '%Y-%m-%d')

        if user.institution and user.type in [2, 3]:
            year, week, weekday = catalog_util.get_year_and_week(date)
            start, end = catalog_util.get_start_end_dates(year, week)

            query = catalog_model.Workout.objects.filter(
                day__week__number_week=week,
                institution=institution,
                active=True,
                has_library=False
            )

            if teams and not athletes:
                data = []
                for team in teams:
                    workouts = [workout for workout in query if int(team) == workout.team.id]
                    team = get_object_or_404(team_model.Team, pk=int(team))
                    team_calendar = {}
                    team_calendar["item"] = serializer_team.TeamCustomSerializer(team).data
                    team_calendar["data"] = []
                    for workout in workouts:
                        team_calendar["data"].append(serializers.TeamCalendarSerializer(workout).data)
                    data.append(team_calendar)


                # for team in teams:
                #     workouts = [workout for workout in query if int(team) == workout.team.id]

                #     for workout in workouts:
                #         for athlete in workout.athletes:
                #             exist = False
                #             position = None
                #             for index, obj in enumerate(data):
                #                 if obj["item"] and athlete.id == int(obj["item"]["id"]):
                #                     exist = True
                #                     position = index
                #                     break
                #             if exist:
                #                 data[position]["data"].append(serializers.TeamCalendarSerializer(workout).data)                    
                #             else:
                #                 athlete_calendar = {}                                
                #                 athlete_calendar["item"] = serializers.AthleteCalendarSerializer(athlete).data
                #                 athlete_calendar["data"] = []
                #                 athlete_calendar["data"].append(serializers.TeamCalendarSerializer(workout).data)
                #                 data.append(athlete_calendar)

                # for team in teams:
                #     workouts = [workout for workout in query if int(team) == workout.team.id]
                #     team = get_object_or_404(team_model.Team, pk=int(team))
                #     team_calendar = {}
                #     team_calendar["item"] = serializer_team.TeamCustomSerializer(team).data
                #     team_calendar["data"] = []
                #     for workout in workouts:
                #         team_calendar["data"].append(serializers.TeamCalendarSerializer(workout).data)
                #     data.append(team_calendar)

                return Response(data)

            if teams and athletes:
                data = []
                team = get_object_or_404(team_model.Team, pk=int(teams[0]))
                for athlete in athletes:
                    workouts = [workout for workout in query if workout.athletes.filter(id=int(athlete)).exists()]
                    athlete = get_object_or_404(security_model.User, pk=int(athlete))
                    athlete_calendar = {}
                    athlete_calendar["item"] = serializer_team.TeamCustomSerializer(team).data
                    athlete_calendar["data"] = []
                    for workout in workouts:
                        item = serializers.TeamCalendarSerializer(workout).data
                        item["athletes"] = []
                        item["athletes"].append(serializers.AthleteCalendarSerializer(athlete).data)
                        athlete_calendar["data"].append(item)

                    data.append(athlete_calendar)

                # for athlete in athletes:
                #     workouts = [workout for workout in query if workout.athletes.filter(id=int(athlete)).exists()]
                #     athlete = get_object_or_404(security_model.User, pk=int(athlete))
                #     athlete_calendar = {}
                #     athlete_calendar["item"] = serializers.AthleteCalendarSerializer(athlete).data
                #     athlete_calendar["data"] = []
                #     for workout in workouts:
                #         athlete_calendar["data"].append(serializers.TeamCalendarSerializer(workout).data)
                #     data.append(athlete_calendar)

                return Response(data)

            teams_calendar = []
            for workout in query:
                exist = False
                position = None
                for index, obj in enumerate(teams_calendar):
                    if workout.team and obj["item"] and workout.team.id == int(obj["item"]["id"]):
                        exist = True
                        position = index
                        break
                if exist:
                    teams_calendar[position]["data"].append(serializers.TeamCalendarSerializer(workout).data)                    
                else:
                    team_calendar = {}
                    if workout.team:
                        team = get_object_or_404(team_model.Team, pk=workout.team.id)
                        team_calendar["item"] = serializer_team.TeamCustomSerializer(team).data
                    else:
                        team_calendar["item"] = None
                    team_calendar["data"] = []
                    team_calendar["data"].append(serializers.TeamCalendarSerializer(workout).data)
                    teams_calendar.append(team_calendar)

            return Response(teams_calendar)
        return Response([])

class CalendarWorkoutUpdateView(APIView):
    @transaction.atomic
    def patch(self, request, pk, format=None):
        date = request.data.get('date', None)
        if not date:
            raise exceptions.ValidationError(_('A date is required.'))

        instance = get_object_or_404(catalog_model.Workout, pk=pk)
        program = instance.program
        if not program:
            raise exceptions.ValidationError(_('There is no assigned program.'))

        date = datetime.strptime(date, '%Y-%m-%d')
        year, number_week, number_day = catalog_util.get_year_and_week(date)

        query = catalog_model.Week.objects.filter(
            phase__program=program,
            number_week=number_week,
            active=True,
            has_library=False
        )

        if query:
            week = query.first()
            day = week.week_day.filter(day=number_day)
            if day.exists():
                instance.day = day.first()
                instance.save()
            else:
                day = catalog_model.Day.objects.create(day=number_day, week=week)
                instance.day = day
                instance.save()

            serializer = catalog_serializer.WorkoutSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

            response = {}
            response["item"] = serializer_team.TeamCustomSerializer(instance.team).data
            response["data"] = []
            response["data"].append(serializers.TeamCalendarSerializer(instance).data)

            return Response(response)

        raise exceptions.ValidationError(_('No registered information was found for this week.')) 
