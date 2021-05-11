from django.conf import settings
from django.utils.translation import ugettext as _
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site

from django_filters import rest_framework as filters

from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.views import Response, status, APIView
from rest_framework.decorators import api_view
from rest_framework import exceptions, viewsets
from rest_framework import filters as df

from . import models
from . import serializers
from . import utils
from . import forms

from apps.payments import models as payment_model
from apps.payments import serializers as serializer_payment
from apps.teams import models as team_model

import uuid
import json
from rest_framework.generics import get_object_or_404
from django.contrib import messages
from apps.security.forms import ResetPasswordForm




class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer

class SocialLoginView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = serializers.LoginSocialSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # validate social email
        exist, user = utils.validate_auth_media(
            serializer.validated_data['email'],
            serializer.validated_data['social_type']
            )
        if exist:
            user.full_name = serializer.validated_data['full_name']
            user.save_remote_image(serializer.validated_data['photo'])
            user.save()
            response = utils.get_tokens_for_user(user)
            return Response(response,status=status.HTTP_200_OK)
        else:
            user = models.User.objects.create_user(
                full_name = serializer.validated_data['full_name'],
                email = serializer.validated_data['email'],
                username = serializer.validated_data['email'],
                social_type = serializer.validated_data['social_type'],
                type = serializer.validated_data['type'],
                token_social_login = serializer.validated_data['token_social_login'],
                password = serializer.validated_data['token_social_login'],
                email_verified = True
            )
            user.save()
            user.save_remote_image(serializer.validated_data['photo'])
            response = utils.get_tokens_for_user(user)
            return Response(response,status=status.HTTP_200_OK)
            

class CurrentSubscriptionView(APIView):
    def get(self, request):
        item = payment_model.Subscription.objects.filter(
            institution=self.request.user.institution,
            ).order_by('-created_at').first()
        if item:
            return Response(serializer_payment.SubsciptionListSerializer(item).data,status=status.HTTP_200_OK)
        raise exceptions.ValidationError(_('you don´t have subscriptions'))

class Me(APIView):
    def get(self, request):
        user = request.user
        serializer = serializers.UserDetailSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    def post(self, request):
        serializer = serializers.ChangePassworsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = models.User.objects.filter(pk=serializer.validated_data['id']).first()
            if user:
                if user.social_type != 4:
                    raise exceptions.ValidationError(_('this user not change password because social login has'))
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response(status=status.HTTP_200_OK)
        else:
            raise exceptions.ValidationError(serializer.errors)
            

class UserResetPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        type = request.data.get('type')
        if not email:
            raise exceptions.ValidationError(_('email field is required.'))
        else:
            user = models.User.objects.filter(
                email=email, 
                is_active=True, 
                email_verified=True)
            if type:
                user = user.filter(type=type).first()
            else:
                user = user.first()
            if user:
                if user.social_type != 4:
                    raise exceptions.ValidationError(_('this user not change password because social login has'))
                utils.send_reset_password_email_reset(user, site=get_current_site(request))
                return Response({'email': email}, status=status.HTTP_200_OK)
            else:
                raise exceptions.ValidationError(_('email not found or user is not active'))

def reset_password_user(request, token):
    if request.method == 'POST':
        form = forms.ResetPasswordForm(request.POST)
        user = models.User.objects.filter(activation_token=token).first()
        if not user:
            form = forms.ResetPasswordForm()
            messages.error(request, _('The link to change password is not valid.'))
            return render(request, 'set_password.html', {
                'form': form,
                'error': _('Reset password'),
                'title': _('Welcome to Solo Performance, please set password and confirm password'),
                'team': _('Team'),
                })
        
        if not user.is_active or not user.email_verified:
            form = forms.ResetPasswordForm()
            messages.error(request, _('This user is not active'))
            return render(request, 'set_password.html', {
                'form': form,
                'error': _('Reset password'),
                'title': _('Welcome to Solo Performance, please set password and confirm password'),
                'team': _('Team'),
                })
        
        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            user.set_password(new_password)
            user.activation_token = uuid.uuid4()
            user.save()
            return HttpResponseRedirect(settings.URL_PANEL)
    else:
        
        form = ResetPasswordForm(initial={'token': token})

    return render(request, 'set_password.html', {
        'form': form,
        'error': _('Reset password'),
        'title': _('Welcome to Solo Performance, please set password and confirm password'),
        'team': _('Team'),
        })
    
class UserView(viewsets.ModelViewSet):
    queryset = models.User.objects.all().exclude(is_staff=True)
    serializer_class = serializers.UserDetailSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('type', 'region', 'gender', 'institution', 'is_active')
    search_fields = ('full_name','email','username',)
    
    def perform_update(self, serializer):
        email = self.request.data.get('email')
        if email:
            item = serializer.save(
                username = email,
                last_edited = self.request.user
            )
        else:
            item = serializer.save(
                last_edited = self.request.user
            )
        return item
    
class UserTeamView(viewsets.ReadOnlyModelViewSet):
    queryset = models.User.objects.all().exclude(is_staff=True)
    serializer_class = serializers.CustomTeamSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('type', 'region', 'gender', 'institution', 'is_active')
    search_fields = ('full_name','email','username','birthday')
    

class LibraryUserView(viewsets.ReadOnlyModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.LibraryUserSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('type', 'region', 'gender', 'institution', 'is_active')
    search_fields = ('full_name','email','username','birthday')
    ordering_fields = ('full_name','email','type','birthday','updated_at',)
    
    def get_queryset(self):
        return models.User.objects.filter(type__in=[2,3])

class LibraryAthleteView(viewsets.ReadOnlyModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.AthleteUserSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('type', 'region', 'gender', 'institution', 'is_active')
    search_fields = ('full_name','email','username','birthday')
    ordering_fields = ('full_name','email','type','birthday','updated_at',)
    
    def get_queryset(self):
        return models.User.objects.filter(type__in=[4])
    
class LibraryCoachView(viewsets.ReadOnlyModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.TeamUserSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('type', 'region', 'gender', 'institution', 'is_active')
    search_fields = ('full_name','email','username','birthday')
    ordering_fields = ('full_name','email','type','updated_at',)
    
    def get_queryset(self):
        return models.User.objects.filter(type__in=[3])
    

    
class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        type = self.request.data.get('type',0)
        if int(type) != 4:
            raise exceptions.ValidationError(_('this type of user is invalid'))
        serializer = serializers.UserCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.email = user.email.lower()
        user.username = user.email
        user.is_active = False
        user.email_verified = False
        user.save()
        if settings.CUSTOM_REGISTRATION.get('SEND_ACTIVATION_EMAIL', False):
            utils.send_activation_email(
                user_email=user.email,
                activation_code=user.activation_token,
                site=get_current_site(request)
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserCreate(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        user_request = self.request.user
        permission = utils.validate_permissions(user_request,self.request.data.get('type'))
        if not permission:
            raise exceptions.ValidationError(_('you dont have permissions for create this user'))
        serializer = serializers.UserCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.email = user.email.lower()
        user.username = user.email
        user.is_active = False
        user.email_verified = False
        user.last_edited = user_request
        user.save()
        team = self.request.data.get('team')
        if team:
            team = team_model.Team.objects.filter(pk=int(team)).first()
            if team: 
                if user.type == 2:
                    team.institution_managers.add(user)
                if user.type == 3:
                    team.coaches.add(user)
                if user.type == 4:
                    team.athletes.add(user)
        if user.type in [1,2,3,4]:
            if settings.CUSTOM_REGISTRATION.get('SEND_ACTIVATION_EMAIL', False):
                utils.send_activation_email(
                    user_email=user.email,
                    activation_code=user.activation_token,
                    site=get_current_site(request)
                )
        else:
            user.is_active = True
            user.email_verified = True
            user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
def activation(request, activation_token,see=True):
    try:
        user = models.User.objects.get(activation_token=activation_token)
        if user.type == 4:
            see=False
        if not user.is_active:
            user.is_active = True
            user.email_verified = True
            user.activation_token = uuid.uuid4()
            user.save()
        return render(request, 'activation.html', context={
            'error': _('Account active!!'),
            'title': _('Welcome to Solo Performance, your account has been activated'),
            'panel': _('Go to panel'),
            'team': _('Team'),
            'url_panel': settings.URL_PANEL,
            'see':see
            })
    except models.User.DoesNotExist:
        return render(request, 'error_page.html', context={
            'error': _('This link is not valid'),
            'title': _('Oops something went wrong'),
            'team': _('Team'),
            
        })



# Function 404
def error_404_def(request, exception):
    data = {
        'message': 'Endpoint was not found or has been removed',
        'code': 1019
    }

    return HttpResponse(
        json.dumps(data), content_type='application/json', status=400
    )

@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def error_404_view(request):
    # print(request.method)

    try:
        return Response(
            {
                'message': 'Endpoint was not found or has been removed',
                'code': 1019
            },
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        print(e)
        return Response(None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
