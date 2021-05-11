# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('send_push/', views.send_push),
    path('home/', views.home),

]