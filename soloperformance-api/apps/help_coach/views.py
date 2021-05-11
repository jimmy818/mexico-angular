from django.shortcuts import render
from rest_framework import filters as df, mixins, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.help_coach import  models as models_help
from apps.coach import models as models_coach, serializers as serializer_coach,utils as utils_coach
from .  import  serializers
from apps.catalog import models as models_catalog
from apps.help_coach import training_phase
from  django.db.models.signals import post_save
import json
# Create your views here.
from webpush import send_user_notification


   
class HelpCoachTrainigAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    queryset = models_help.ProgramWorkouts.objects.all()
    serializer_class = serializers.ProgramWorkoutsSerializer
    search_fields = ('program',)
 
    
    def get(self, request):
        program_id = request.data["program"]
        program_get= models_help.ProgramWorkouts.objects.filter(program=program_id).first()        
        if program_get:
            
            serializer_class = serializers.ProgramWorkoutsSerializer(program_get)
            return Response(serializer_class.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
    def post(self,request):
        program = request.data["program"]
        
        if models_help.ProgramWorkouts.objects.filter(program=program).exists() :
            model = models_help.ProgramWorkouts.objects.filter(program=program).first()
            serializer_class = serializers.ProgramWorkoutsSerializer(model)   
          
            return Response(serializer_class.data)
            
        else:
            program_coach = models_catalog.Program.objects.filter(pk=program).filter(active=True).first()
           
            model = models_help.ProgramWorkouts()
            model.program=program_coach
            model.workouts_program={}
            model.save()
            model_new = models_help.ProgramWorkouts.objects.filter(program=program_coach).first()

            serializer_class = serializers.ProgramWorkoutsSerializer(model_new)   
            return Response( serializer_class.data,status=status.HTTP_200_OK)
       
    
    
class RegionsCategoryProgramView(APIView):
   
    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RegionsCategoryCoachSerializer
        return self.serializer_class
    
    def perform_create(self, serializer):
        item = serializer.save()
        return item
    
    def get(self, request, *arg, **kwargs):
        queryset= models_help.RegionsCategoryCoach.objects.all()
        serializer_class = serializers.RegionsCategoryCoachSerializer(queryset, many=True)
        return Response( serializer_class.data, status=status.HTTP_200_OK)

    
    
    def post (self, request , *arg, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = serializers.RegionsCategoryCoachSerializer(instance,many=True)
        return Response(instance_serializer.data)
    
class VariationVerticalPhaseViews(APIView):              

    def get(self,request):
        serializer = models_help.VariationVertical.objects.all()
        serializer__class= serializers.VariationVerticalSerializer(serializer, many=True)
                  
        return Response(serializer__class.data ,status = status.HTTP_200_OK)
    
    def post(self, request):
        variation_vertical= self.request.data.get["variation_vertical"]
        phase = request.data.get['phase']
        model_phase = models_catalog.Phase.objects.filter(pk= phase).first()
        model_variation =  models_help.VariationVertical.objects.filter(pk=variation_vertical).first()
        print(request.data) 
        model_variation_phase = models_help.VariationVerticalProgram(
            phase =model_phase,
            variation=model_variation
        )
          
        model_variation_phase.save()
        model_serializer = serializers.VariationVerticalProgramSerializer(model_variation_phase)
        return Response(model_serializer.data, status=status.HTTP_201_CREATED)
    
    

class VariationHorizontalViews(APIView):
    
    
    def get(self, request):
        serializer = models_help.VariationHorizontal.objects.all()
        serializer_class =  serializers.VariationHorizontalSerializer(serializer, many =True)
        return Response(serializer_class.data,status=status.HTTP_200_OK)
        
    def post(self, request):
        print(request.data)
        
        return Response(request.data,status=status.HTTP_200_OK)