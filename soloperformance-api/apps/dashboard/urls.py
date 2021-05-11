from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from . import views


router = DefaultRouter()

router.register('widget',views.WidgetView)
router.register('current-widgets',views.CustomWidgetView)
router.register('events',views.EventView)
router.register('events-text',views.EventPosterView)


urlpatterns = [
    path('events-filter/', views.EventFilterView.as_view()),
    path('events-list/', views.EventListView.as_view()),
    path('calendar-list/', views.CalendarListView.as_view()),
    path('move-workout/<int:pk>/', views.CalendarWorkoutUpdateView.as_view()),
    
]

urlpatterns += router.urls
