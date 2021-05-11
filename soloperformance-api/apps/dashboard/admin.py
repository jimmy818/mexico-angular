from django.contrib import admin
from . import models
from django.utils.translation import ugettext as _
# Register your models here.

@admin.register(models.Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ['name',]

@admin.register(models.UserWidget)
class UserWidgetAdmin(admin.ModelAdmin):
    list_display = ('user', )
    
@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(models.EventPoster)
class EventPosterAdmin(admin.ModelAdmin):
    list_display = ('name', )








