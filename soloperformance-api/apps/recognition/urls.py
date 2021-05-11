
from . import views
from django.urls import path


urlpatterns = [
    
    path('recognition/', views.viewImage),
    
]

