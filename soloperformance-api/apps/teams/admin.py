from django.contrib import admin
from . import models
from django.utils.translation import ugettext as _
# Register your models here.

@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):

    list_display = ('name', )
    search_fields = ['name','institution']
    filter_horizontal = ('institution_managers','athletes','coaches')
    # raw_id_fields = ("institution",)
    # list_select_related = ("institution",)


@admin.register(models.Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at','revenue','active')
    search_fields = ['name',]
    readonly_fields=('identifier_name',)






