from django.db.models.signals import post_save
from .models import MemberModel, OrganizationModel


def create_member(sender, instance, created, **kwargs):
    """Member Creation Automatically after Org Creation"""
    if created:
        member = MemberModel.objects.create(org=instance, name='Family')
        member.save()


post_save.connect(create_member, sender=OrganizationModel)
