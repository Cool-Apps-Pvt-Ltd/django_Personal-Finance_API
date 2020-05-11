from django.db.models.signals import post_save
from .models import Income, MonthYear

"""
@todo
1. create_month_year
 - Incase of create in get_or_create, decide what to assign for Currency
"""


def create_month_year(sender, instance, created, **kwargs):
    """MonthYear Object is created if it doesn't exist"""
    if created:
        MonthYear.objects.get_or_create(month=instance.month,
                                        year=instance.year,
                                        org=instance.org)


post_save.connect(create_month_year, sender=Income)
