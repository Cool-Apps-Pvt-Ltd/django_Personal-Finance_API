from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from .models import UserProfile, OrganizationModel, MemberModel


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id', 'first_name',
                    'last_name', 'email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important Dates'), {'fields': ('last_login',)})
    )


# Register models here.
admin.site.register(UserProfile, UserAdmin)
admin.site.register(OrganizationModel)
admin.site.register(MemberModel)
