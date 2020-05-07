from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import *

def create_member(sender, instance, created, **kwargs):
    """Member Creation Automatically after Org Creation"""
    if created:
        member = MemberModel.objects.create(org=instance, name='Family')
        member.save()

post_save.connect(create_member, sender=OrganizationModel)
