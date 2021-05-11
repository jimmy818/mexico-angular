from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _
from .models import User

# admin.site.register(User, FleteroAdmin)


@admin.register(User)
class MyUserAdmin(UserAdmin):

    fieldsets_admin = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'email','phone','region','institution','last_edited','social_type','weigth','heigth','FCM','MSS','MAS','gender','birthday')}),
    )

    list_display = ('type', 'full_name', 'email', 'is_active', 'email_verified', 'created_at',)
    list_filter = ('type', 'is_active', 'is_staff', 'email_verified',)
    search_fields = ['full_name', 'email']
    ordering = ['email', ]
    fieldsets = fieldsets_admin + (
            ('Información operativa', {'fields': (
                                        'type',
                                        'photo',
                                        'activation_token'
            )}),
            (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'email_verified')}),
    )
    readonly_fields = UserAdmin.readonly_fields
