from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()


urlpatterns = [
    path('files-exersice/', views.FilesToS3.as_view()),

    
]


urlpatterns += router.urls
