from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views



router = DefaultRouter()
router.register('workout-list', views.WorkoutlistAPIView, basename="workout")
router.register('training-level', views.TriningLevel)
router.register('catalog-level', views.NivelCatalogView)

urlpatterns = [
    path('workout/', views.WorkoutAPIView.as_view()),
    path('workout-express/', views.WorkoutExpressAPIView.as_view()),
    path('nivel/', views.NivelAPIView.as_view()),
    path('category-selection/', views.CategorySelectionNivelUserAPIView.as_view()),
    path('nivel-user/', views.NivelUserApiView.as_view()),
    path('goals-user/<int:level>/', views.GoalsUserView.as_view()),
    path('goals-user/', views.GoalsUserView.as_view()),
    path('equipment-user/', views.EquipUserView.as_view())
    
]

urlpatterns += router.urls
