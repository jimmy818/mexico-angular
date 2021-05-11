from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from . import views


router = DefaultRouter()
router.register('user',views.UserView)
router.register('user-team',views.UserTeamView)
router.register('users-library',views.LibraryUserView)
router.register('athletes-library',views.LibraryAthleteView)
router.register('coaches-library',views.LibraryCoachView)



urlpatterns = [
    path('token-refresh/', TokenRefreshView.as_view()),
    path('token/', views.MyTokenObtainPairView.as_view()),
    path('social-login/', views.SocialLoginView.as_view()),
    path('users/', views.UserCreate.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('activate/<uuid:activation_token>/', views.activation),
    path('current-subscription', views.CurrentSubscriptionView.as_view()),
    path('change-password/', views.ChangePasswordView.as_view()),
    path('reset-password/', views.UserResetPassword.as_view()),
    path('reset-password/<uuid:token>/', views.reset_password_user),
    path('me', views.Me.as_view()),
]

urlpatterns += router.urls
