from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from . import views

router = DefaultRouter()


urlpatterns = [
    path('help-coach/',views.HelpCoachTrainigAPIView.as_view()),
    path('program-category/',views.RegionsCategoryProgramView.as_view()),
    path('variation-vertical/',views.VariationVerticalPhaseViews.as_view()),
    path('variation-horizontal/',views.VariationHorizontalViews.as_view()),


]


urlpatterns += router.urls
