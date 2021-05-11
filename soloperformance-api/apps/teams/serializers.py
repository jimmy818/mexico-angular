from rest_framework import serializers, exceptions
from . import models
from apps.payments import models as model_payments
from apps.payments import serializers as serializer_payment
from apps.security import serializers as serializer_user



class TeamListSerializer(serializers.ModelSerializer):
    institution_managers = serializer_user.TeamUserSerializer(many=True)
    athletes = serializer_user.TeamUserSerializer(many=True)
    coaches = serializer_user.TeamUserSerializer(many=True)
    updated_by = serializer_user.TeamUserSerializer()
    class Meta:
        model = models.Team
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = '__all__'



class TeamCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ('id','name','image')


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Institution
        fields = '__all__'

class InstitutionLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Institution
        fields = ('id','name')

class TeamProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ('id','image','name')
    

class InstitutionListSerializer(serializers.ModelSerializer):
    subscription = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Institution
        fields = '__all__'
    
    def get_subscription(self, instance):
        item = model_payments.Subscription.objects.filter(
            institution=instance.id).order_by('-created_at').first()
        if item:
            return serializer_payment.SubsciptionListSerializer(item).data
        else:
            return None
    
class CustomUserAddSerializer(serializers.Serializer):
    type = serializers.IntegerField(required=True)
    team = serializers.IntegerField(required=True)
    user = serializers.IntegerField(required=True)
        