from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from personal_finance_api.models import OrganizationModel, MemberModel
from .constants import CURRENCIES, INCOME_SOURCE

"""
Features
##########
1. MonthYear Model
 - Foreign Key is Org. Independent Model to summarize data from other Child models for org
 - No other Model is a direct child to this Model
 
2. Income Model
 - Collects Income transactions for home org members
 - Member and Org are foreign keys. Income is deleted on their deletion

@todo
#########
1. Income model
 - Add signals and connector to create MonthYear entry if it doesnt exist
 
"""


class MonthYear(models.Model):
    """Month-Year Model for data aggregation from other models"""
    month = models.IntegerField(default=datetime.today().month,
                                validators=[
                                    MinValueValidator(1),
                                    MaxValueValidator(12)
                                ],
                                blank=False)
    year = models.IntegerField(default=datetime.today().year,
                               validators=[
                                   MinValueValidator(2000),
                                   MaxValueValidator(2200)
                               ],
                               blank=False)
    primary_currency = models.CharField(default='INR',
                                        choices=CURRENCIES,
                                        max_length=3)
    is_locked = models.BooleanField(default=False,
                                    blank=False)

    # Keys
    org = models.ForeignKey(OrganizationModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('month', 'year', 'org')
        index_together = ('month', 'year', 'org')


class Income(models.Model):
    """Income Model to save income transactions"""
    income_source = models.CharField(default='Salary',
                                     choices=INCOME_SOURCE,
                                     blank=False,
                                     max_length=10)
    income_before_tax = models.FloatField(default=0.0, blank=False)
    tax_withheld = models.FloatField(default=0.0, blank=False)
    deductions = models.FloatField(default=0.0, blank=False)
    currency = models.CharField(default='INR',
                                choices=CURRENCIES,
                                max_length=3)
    last_updated_on = models.DateField(auto_now_add=True)
    month = models.IntegerField(default=datetime.today().month,
                                validators=[
                                    MinValueValidator(1),
                                    MaxValueValidator(12)
                                ],
                                blank=False)
    year = models.IntegerField(default=datetime.today().year,
                               validators=[
                                   MinValueValidator(2000),
                                   MaxValueValidator(2200)
                               ],
                               blank=False)

    # Keys
    member = models.ForeignKey(MemberModel, on_delete=models.CASCADE)
    org = models.ForeignKey(OrganizationModel, on_delete=models.CASCADE)

    class Meta:
        index_together = ('member', 'org')


#################
# Backend models
##################
class CurrencyConverter(models.Model):
    """Currency conversion database """
    currency = models.CharField(choices=CURRENCIES, max_length=3, blank=False)
    # Value of one USD in the currency listed above
    one_dollar_in_currency = models.FloatField(blank=False, validators=[MinValueValidator(0)])

    # Keys
    conversion_month = models.ForeignKey(MonthYear, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('currency', 'conversion_month'))
        index_together = (('currency', 'conversion_month'))
