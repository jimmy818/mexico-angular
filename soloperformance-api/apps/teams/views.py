from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _

from rest_framework import viewsets
from rest_framework import filters as df
from rest_framework import exceptions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django_filters import rest_framework as filters

from . import models
from . import serializers

from apps.payments import serializers as serializer_payment
from apps.payments import models as model_payment
from apps.security import serializers as user_serializer
from apps.security import models as user_model

from . import utils as utils_team

# Create your views here.


class ReadTeamView(viewsets.ReadOnlyModelViewSet):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamListSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('active','institution')
    search_fields = ('name', )
    
    def get_queryset(self):
        user  = self.request.user
        if user.type == 1:
            return models.Team.objects.filter(institution__isnull=False)
        else:
            return models.Team.objects.filter(institution__isnull=False,institution=user.institution)
        items = models.Team.objects.filter(institution=user.institution,institution__isnull=False)
        return items

class ReadTeamWidgetView(ReadTeamView):
    serializer_class = serializers.TeamCustomSerializer
    pagination_class = None

class TeamView(viewsets.ModelViewSet):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    
    def perform_create(self, serializer):
        institution = self.request.data.get('institution')
        subscription = model_payment.Subscription.objects.filter(institution=int(institution),is_active=True).first()
        if not subscription:
            raise exceptions.ValidationError(_('this institution not has active subscription'))
        total_team = models.Team.objects.filter(institution=int(institution)).count()
        if total_team >= subscription.total_team:
            raise exceptions.ValidationError(_('this institution has limit of teams created'))
        item = serializer.save()
        item.updated_by = self.request.user
        item.save()
        return item

class TeamProfileView(viewsets.ReadOnlyModelViewSet):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamProfileSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('institution',)


class AthletesProfileView(viewsets.ReadOnlyModelViewSet):
    queryset = user_model.User.objects.all()
    serializer_class = user_serializer.TeamUserSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    search_fields = ('full_name',)

    def get_queryset(self):
        team_id = self.request.query_params.get('team', None)
        if team_id:
            team = get_object_or_404(models.Team, pk=team_id)
            if team.athletes.count():
                return team.athletes.all().order_by('full_name')
        return []


class ReadInstitutionView(viewsets.ReadOnlyModelViewSet):
    queryset = models.Institution.objects.all()
    serializer_class = serializers.InstitutionListSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('name',)
    search_fields = ('name', )
    ordering_fields = ('name','id','type','created_at','active',)
    def get_queryset(self):
        user  = self.request.user
        if not user.type in [1,2]:
            raise exceptions.ValidationError(_('you don´t have permissions'))
        return super().get_queryset()
    
class IntitutionView(viewsets.ModelViewSet):
    queryset = models.Institution.objects.all()
    serializer_class = serializers.InstitutionSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('name',)
    search_fields = ('name', )
    
    def get_queryset(self):
        user  = self.request.user
        if not user.type in [1,2]:
            raise exceptions.ValidationError(_('you don´t have permissions'))
        return super().get_queryset()
    
    
    def perform_create(self, serializer):
        user  = self.request.user
        if not user.type in [1,2]:
            raise exceptions.ValidationError(_('you don´t have permissions'))
        type = self.request.data.get('type',None)
        if type:
            subscription_validate = serializer_payment.SubsciptionValidateSerializer(data=self.request.data)
            subscription_validate.is_valid(raise_exception=True)
            item = serializer.save(
                revenue=self.request.data.get('total',0.0)
                )
            subscription = subscription_validate.save(
                is_active=True
            )
            subscription.institution = item
            subscription.save()
        else:
            item = serializer.save()
        return item

class InstitutionDetailView(APIView):
    
    def get(self, request, pk):
        institution_managers = utils_team.get_user_managers(pk, 2)
        strength_coaches = utils_team.get_user_managers(pk, 3)
        

        
        data = {
            'institution_managers' : institution_managers,
            'strength_coaches' : strength_coaches,
            'institution_stats': {
                'system_time_used' : None,
                'created_athletes' : 0,
                'monthly_login': 0,
            },
            'revenue': {
                'monthly_revenue':0,
                'tax': 0,
                'total_revenue': 0
            },
            'economic' :{
                'arpu': 0,
                'clv':0,
                'rate':0
            }
        }
        
        return Response(data,status=status.HTTP_200_OK)

class CustomUserTeamView(APIView):
    
    def get(self, request, pk):
        '''
        1 : atlhetes
        2 : coaches coaches
        3 : institution managers  institution_managers
        '''
        type = self.request.GET.get('type')
        institution = models.Team.objects.filter(pk=pk).first()
        if institution:
            if int(type) == 1:
                atletes = institution.athletes.all()
                serializer = user_serializer.CustomTeamSerializer(atletes,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            if int(type) == 2:
                coaches = institution.coaches.all()
                serializer = user_serializer.CustomTeamSerializer(coaches,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            if int(type) == 3:
                institution_managers = institution.institution_managers.all()
                serializer = user_serializer.CustomTeamSerializer(institution_managers,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)

class AddCustomUserTeamView(APIView):
    
    def post(self, request):
        '''
        1 : atlhetes
        2 : coaches coaches
        3 : institution managers  institution_managers
        '''
        serializer = serializers.CustomUserAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = models.Team.objects.filter(pk=serializer.validated_data['team']).first()
        user = user_model.User.objects.filter(pk=serializer.validated_data['user']).first()
        
        if serializer.validated_data['type'] == 1:
            atletes = team.athletes.all()
            if not user in atletes:
                team.athletes.add(user)
                team.updated_by = self.request.user
                team.save()
            return Response(status=status.HTTP_200_OK)
        if serializer.validated_data['type'] == 2:
            coaches = team.coaches.all()
            if not user in coaches:
                team.coaches.add(user)
                team.updated_by = self.request.user
                team.save()
            return Response(status=status.HTTP_200_OK)
        if serializer.validated_data['type'] == 3:
            institution_managers = team.institution_managers.all()
            if not user in institution_managers:
                team.institution_managers.add(user)
                team.updated_by = self.request.user
                team.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)


class RemoveCustomUserTeamView(APIView):
    
    def post(self, request):
        '''
        1 : atlhetes
        2 : coaches coaches
        3 : institution managers  institution_managers
        '''
        serializer = serializers.CustomUserAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = models.Team.objects.filter(pk=serializer.validated_data['team']).first()
        user = user_model.User.objects.filter(pk=serializer.validated_data['user']).first()
        print(self.request.user)
        
        if serializer.validated_data['type'] == 1:
            atletes = team.athletes.all()
            if  user in atletes:
                team.athletes.remove(user)
                team.updated_by = self.request.user
                team.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if serializer.validated_data['type'] == 2:
            coaches = team.coaches.all()
            if user in coaches:
                team.coaches.remove(user)
                team.updated_by = self.request.user
                team.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if serializer.validated_data['type'] == 3:
            institution_managers = team.institution_managers.all()
            if user in institution_managers:
                team.institution_managers.remove(user)
                team.updated_by = self.request.user
                team.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_204_NO_CONTENT)


        

