"""performance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls import handler404, handler403
from django.urls import path
from django.views.generic import TemplateView
from apps.security import views
from apps.security.views import error_404_view

api_url = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{api_url}', include('apps.payments.urls')),
    path(f'{api_url}', include('apps.catalog.urls')),
    path(f'{api_url}', include('apps.security.urls')),
    path(f'{api_url}', include('apps.regions.urls')),
    path(f'{api_url}', include('apps.teams.urls')),
    path(f'{api_url}', include('apps.dashboard.urls')),
    path(f'{api_url}', include('apps.coach.urls')),
    path(f'{api_url}', include('apps.survey.urls')),
    path(f'{api_url}', include('apps.s3files.urls')),
    path(f'{api_url}', include('apps.notifications.urls')),

    # path(f'{api_url}', include('apps.recognition.urls')),
    path(f'{api_url}', include('apps.help_coach.urls')),
    path('webpush/', include('webpush.urls')),
    path(f'{api_url}sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript')),


    path('', TemplateView.as_view(template_name='default_urlconf.html'), name="index"),
]

handler404 = views.error_404_def    

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )


admin.site.site_header = settings.APPNAME
