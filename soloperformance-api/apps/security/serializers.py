
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import ugettext as _
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers



from . import models


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['permission'] = {
            'type': self.user.type,
            'str_type': self.user.get_type_display(),
        }
        if self.user.institution:
            data['institution'] = self.user.institution.id
        else:
            data['institution'] = None
        
        return data

class InstitutionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'id',   
            'full_name',
        )


class LoginSocialSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=True)
    photo = serializers.CharField(required=True)
    type = serializers.IntegerField(required=True)
    social_type = serializers.IntegerField(required=True)
    token_social_login = serializers.CharField(required=True)

class TeamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'id',   
            'photo',
            'full_name',
            'email',
            'birthday',
        )

class CustomTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'id',
            'photo',
            'full_name',
            'email',
            'birthday'
        )

class LibraryUserSerializer(serializers.ModelSerializer):
    last_edited = TeamUserSerializer()
    class Meta:
        model = models.User
        fields = (
            'id',   
            'full_name',
            'email',
            'photo',
            'phone',
            'birthday',
            'type',
            'last_edited',
            'updated_at',
            'is_active'
        )

class AthleteUserSerializer(serializers.ModelSerializer):
    teams = serializers.SerializerMethodField(read_only=True)
    last_edited = TeamUserSerializer()
    class Meta:
        model = models.User
        fields = (
            'id',   
            'full_name',
            'email',
            'photo',
            'birthday',
            'weigth',
            'heigth',
            'phone',
            'last_edited',
            'updated_at',
            'is_active',
            'teams'
        )
    def get_teams(self, instance):
        from apps.teams import models as model_teams
        from apps.teams import serializers as serializers_teams
        item = model_teams.Team.objects.filter(
            athletes=instance).distinct()
        if item:
            return serializers_teams.TeamProfileSerializer(item,many=True).data
        else:
            return []
    
class ChangePassworsSerializer(serializers.Serializer):
    confirm_password = serializers.CharField(required=False)
    password = serializers.CharField(required=True)
    id = serializers.IntegerField(required=True)
    
    def validate_password(self, value):
        request = self.context.get('request', None)
        confirm_password = request.data.get('confirm_password', None)

        if confirm_password != value:
            raise serializers.ValidationError(_('Passwords do not match.'))
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e)
        return value

class UserDetailSerializer(serializers.ModelSerializer):
    institution = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.User
        fields = (
            'id',            
            'type',
            'region',
            'full_name',
            'country_code',
            'phone',
            'gender',
            'birthday',
            'photo',
            'email',
            'institution',
            'username',
            'email_verified',
            'is_active',
            'heigth',
            'weigth',
            'FCM',
            'MSS',
            'MAS'
        )

    def get_institution(self, instance):
        from apps.teams import models as model_teams
        from apps.teams import serializers as serializers_teams
        if instance.institution:
            return serializers_teams.InstitutionListSerializer(instance.institution).data
        else:
            None

class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    class Meta:
        model = models.User
        fields = (
            'id',            
            'type',
            'region',
            'full_name',
            'country_code',
            'phone',
            'gender',
            'birthday',
            'photo',
            'email',
            'institution',
            'username',
            'password',
            'email_verified',
            'is_active',
            'heigth',
            'weigth'
        )
        extra_kwargs = {
            'is_staff': {'read_only': True},
            'username': {'read_only': True},
            'subscription_active': {'read_only': True},
            }


    def create(self, validated_data):
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_email(self, value):
        value = value.lower()
        user = models.User.objects.filter(email=value).exists()
        if user:
            raise serializers.ValidationError(_('The email: %(value)s is already registered.') % {'value': value})
        return value

    def validate_password(self, value):
        request = self.context.get('request', None)
        confirm_password = request.data.get('confirm_password', None)

        if confirm_password != value:
            raise serializers.ValidationError(_('Passwords do not match.'))
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e)

        return value