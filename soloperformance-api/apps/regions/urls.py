from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from . import views


router = DefaultRouter()
router.register('regions',views.RegionListView)


urlpatterns = []

urlpatterns += router.urls
