from django.contrib import admin
from .models import UserProfile, OrganizationModel, MemberModel

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(OrganizationModel)
admin.site.register(MemberModel)