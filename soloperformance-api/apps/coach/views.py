from django.views import generic
from rest_framework.response import Response
from apps.coach.express import training_express
from . Backend import training_total
from . import models, serializers
from . import  utils,build_json
import json
from rest_framework.views import APIView
from rest_framework import filters as df, mixins, status, viewsets, permissions
from django_filters import rest_framework as filters
from rest_framework import exceptions
from django.utils.translation import ugettext as _

from rest_framework import viewsets




class WorkoutlistAPIView(viewsets.ModelViewSet):
    queryset = models.WorkoutNivelPhase.objects.all()
    serializer_class = serializers.WorkoutNivelPhaseSerializer
    search_fields = ('nivel',)
    
    def get_queryset(self):
        return self.queryset.filter(accomplished=True).order_by('id')
    
class WorkoutAPIView(APIView):  
    
    def get(self, request , *arg, **kwargs):
        user = request.user        

        usuario= models.NivelUser.objects.filter(user=user).first()
        equips = models.EquipUser.objects.filter(user=user).values("equipment_id")

    
        equip_user_id =[]
        for equip in equips:
           if equip["equipment_id"]:
                    equip_user_id.append(equip["equipment_id"])
        workout = training_total(user = usuario,
                    equip_user = equip_user_id,                     
                    )
        
        accomplished = False
        workout_new = models.WorkoutNivelPhase(nivel= usuario, workout=workout, accomplished = accomplished)
        
        workout_new.save()
        
        serializer_class = serializers.WorkoutNivelPhaseSerializer (workout,context={'request': request})

        return Response(serializer_class.data, status=status.HTTP_200_OK) 
    
    def post(self,request):
        if request.data.get("id"):
            
            id = request.data.get("id")            
            model = models.WorkoutNivelPhase.objects.get(pk=id)       
            completed = request.data.get("accomplished")
            user_nivel = model.nivel
          
            if completed:
                utils.updated_trainings_user(user_nivel)
                model2 = models.WorkoutNivelPhase.objects.get(pk=id)
                model2.accomplished =  completed
                model2.save()
                serializer_class = serializers.WorkoutNivelPhaseSerializer (model2,context={'request': request})
                utils.updated_nivel(user_nivel)

                return Response( serializer_class.data, status=status.HTTP_200_OK)
            
            serializer_class = serializers.WorkoutNivelPhaseSerializer (model,context={'request': request})

            utils.updated_nivel(user_nivel)

            
        return Response( serializer_class.data, status=status.HTTP_200_OK)
            
   
       
class CategorySelectionNivelUserAPIView(APIView):
    
    def get(self, request):        
        category_selection = models.CategorySelectionNivelUser.objects.all()
        category_selection_serializes = serializers.CategorySelectionNivelUserSerializer(category_selection,  context={'request': request},many =True)
        return Response(category_selection_serializes.data, status=status.HTTP_200_OK)
    
    def get_extra_actions(self):
        if self.action == 'list':
            return serializers.CategorySelectionNivelUser
        return self.extra_actions
    
    def post(self,request):
        
        nivel_user = models.NivelUser.objects.filter(user=request.user).first()
        category= self.request.data.get("category_selection")
        
        category_selection = models.Category.objects.get(pk=category)
        model_category_selection = models.CategorySelectionNivelUser(nivel_user=nivel_user,
                                                                     category_selection=category_selection)
        model_category_selection.save()
        model_serializers = serializers.CategorySelectionNivelUserSerializer(model_category_selection,context={'request': request})
        
        return Response(model_serializers.data,status=status.HTTP_201_CREATED)
    
class NivelAPIView(APIView):
    
    def get(self, request):
        nivel = models.Nivel.objects.all()
        nivel_serializes = serializers.NivelSerializer(nivel, context={'request': request},many =True)
        return Response(nivel_serializes.data, status=status.HTTP_200_OK)

class NivelUserApiView(APIView):
    
    def post(self, request):
        user = request.user
        nivel = models.Nivel.objects.filter(pk=request.data.get("nivel")).first()
        
        nivel_user = models.NivelUser(nivel= nivel, user=user, quantity_trainings= 0)
        nivel_user.save()
        return Response(status=status.HTTP_201_CREATED)
    
    def get(self, request):
        nivel_user = models.NivelUser.objects.all()
        nivel_user_serializers = serializers.NivelUserSerializer(nivel_user, context={'request': request},many=True)
        return Response(nivel_user_serializers.data, status=status.HTTP_200_OK)
    

class WorkoutExpressAPIView(APIView):
    #authentication_classes = []
    #permission_classes = [] 
    def get(self, request , *arg, **kwargs):
        
        user = request.user
        user_nivel= models.NivelUser.objects.filter(user=user).first()
    
        
        workout = training_express(user = user_nivel)
        
        accomplished = False
        
        workout_new = models.WorkoutNivelPhase(nivel= user_nivel, workout=workout, accomplished = accomplished)
        
        workout_new.save()
        
        serializer_class = serializers.WorkoutNivelPhaseSerializer (workout_new,context={'request': request})


        return Response(serializer_class.data, status=status.HTTP_200_OK) 
    
    def post(self,request):
        if request.data.get("id"):
            
            id = request.data.get("id")            
            model = models.WorkoutNivelPhase.objects.get(pk=id)       
            completed = request.data.get("accomplished")
            user_nivel = model.nivel
          
            if completed:
                utils.updated_trainings_user(user_nivel)
                model2 = models.WorkoutNivelPhase.objects.get(pk=id)
                model2.accomplished =  completed
                model2.save()
                serializer_class = serializers.WorkoutNivelPhaseSerializer (model2,context={'request': request})

                return Response( serializer_class.data, status=status.HTTP_200_OK)
            
            serializer_class = serializers.WorkoutNivelPhaseSerializer (model,context={'request': request})

            utils.updated_nivel(user_nivel)

            
            return Response( serializer_class.data, status=status.HTTP_200_OK)


class NivelCatalogView(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    



class TriningLevel(viewsets.ModelViewSet):
    pagination_class = None
    queryset = models.NivelUser.objects.all()
    serializer_class = serializers.NivelUserSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('user',)
    
    def get_queryset(self):
        user = self.request.user
        if user:
            item = models.NivelUser.objects.filter(user=user)
            return item
        return super().get_queryset()
    
    def perform_create(self, serializer):
        user = self.request.user
        if models.NivelUser.objects.filter(user=user).first():
            raise exceptions.ValidationError(_('this user has a previous register saved'))
        return super().perform_create(serializer)

    
class GoalsUserView(APIView):
    
    def post(self, request):
        serializer = serializers.GoalsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        categories = serializer.validated_data['category_selection']
        nivel_user = serializer.validated_data['nivel_user']
        #unactive all registers
        models.CategorySelectionNivelUser.objects.filter(
            nivel_user=nivel_user,
        ).update(active=False)

        for category in categories:
            utils.get_or_create_category_user(nivel_user,category)
        
        # delete all unactives
        models.CategorySelectionNivelUser.objects.filter(
            nivel_user=nivel_user,
            active=False
        ).delete()


        return Response(status=status.HTTP_201_CREATED)
    
    def get(self, request, level):
        nivel = models.CategorySelectionNivelUser.objects.filter(
            nivel_user=level,
            ).values_list('category_selection',flat=True).order_by('category_selection')
        
        return Response(nivel, status=status.HTTP_200_OK)
    
    
    
class EquipUserView(APIView):
    
    
    def post (self ,request):
        serializer = serializers.EquipUserSerializer(data =request.data)
        print(request.data)
        serializer.is_valid()

        equipments = serializer["equipment"]
        user       = serializer["user"]
        for equipment in equipments.value:
           utils.get_or_create_equipment_user(user.value,equipment)
        return Response(status=status.HTTP_201_CREATED)
    

