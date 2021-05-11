from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from . import views


router = DefaultRouter()
router.register('teams',views.TeamView)
router.register('teams-catalog',views.ReadTeamView)
router.register('teams-widget',views.ReadTeamWidgetView)
router.register('institution',views.IntitutionView)
router.register('institution-list',views.ReadInstitutionView)
router.register('team-profile',views.TeamProfileView)
router.register('athletes-profile',views.AthletesProfileView)


urlpatterns = [
    path('info-institution/<int:pk>/', views.InstitutionDetailView.as_view()),
    path('current-user-team/<int:pk>/', views.CustomUserTeamView.as_view()),
    path('current-user-team/', views.AddCustomUserTeamView.as_view()),
    path('remove-user-team/', views.RemoveCustomUserTeamView.as_view()),
]

urlpatterns += router.urls
