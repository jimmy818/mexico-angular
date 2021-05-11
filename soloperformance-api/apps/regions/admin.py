from django.contrib import admin
from . import models
from django.utils.translation import ugettext as _
# Register your models here.

@admin.register(models.Region)
class MyUserAdmin(admin.ModelAdmin):

    list_display = ('name',)
    search_fields = ['name',]

