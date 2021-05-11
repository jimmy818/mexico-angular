from django.urls import path
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from . import views


router = DefaultRouter()

router.register('survey',views.SurveyListView)
router.register('answer',views.AnswerTextView)


urlpatterns = []

urlpatterns += router.urls
