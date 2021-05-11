from rest_framework import serializers
from .  import models
from apps.catalog import serializers as serializers_catalog




class RegionsCategoryCoachSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.RegionsCategoryCoach
        fields = '__all__'
        
class VariationVerticalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VariationVertical
        fields='__all__'
        
class VariationVerticalProgramSerializer(serializers.ModelSerializer):
    variation_vertical =  VariationVerticalSerializer
    phase = serializers_catalog.ProgramPhasesSerializer
    class Meta:
        model = models.VariationVerticalProgram            
        fields = ('id','variation_vertical',"phase")
    
class ProgramWorkoutsSerializer(serializers.ModelSerializer):
    program = serializers_catalog.ProgramPhasesSerializer
    
    class Meta:
        model = models.ProgramWorkouts
        fields = ("id","program","workouts_program")


class VariationHorizontalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VariationHorizontal
        fields= "__all__"