from rest_framework import serializers
from .  import models
from apps.catalog import serializers as serializers_catalog
class WorkoutNivelPhaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.WorkoutNivelPhase
        fields = '__all__'

class NivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Nivel
        fields = '__all__'
        
class CategorySelectionNivelUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CategorySelectionNivelUser
        fields = '__all__'
        
class CustomUserMixin(serializers.Serializer):

    def current_user_default(self):
        request = self.context["request"]
        user = request.user
        return user

    def create(self, validated_data):
        validated_data["user"] = self.current_user_default()
        instance = super().create(validated_data)
        return instance
        
    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.current_user_default()
        # validated_data["active"] = True
        instance = super().update(instance, validated_data)
        return instance



class NivelUserSerializer(CustomUserMixin,serializers.ModelSerializer):
    class Meta:
        model = models.NivelUser
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class GoalsSerializer(serializers.Serializer):
    category_selection = serializers.ListField(required=True)
    nivel_user = serializers.IntegerField(required=True)






class EquipUserSerializer(serializers_catalog.CurrentUserDefaultMixinNotActive,serializers.ModelSerializer):
    equipment = serializers.ListField(required=True)
    user = serializers.IntegerField(required=True)
    class  Meta:
        model = models.EquipUser
        fields = '__all__'