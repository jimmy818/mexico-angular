from django.contrib import admin
from django.utils.translation import ugettext as _
from . import models

# admin.site.register(User, FleteroAdmin)

@admin.register(models.Subscription)
class SubscriptioAdmin(admin.ModelAdmin):
    list_display = ('institution',)





