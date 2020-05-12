from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from personal_finance_api.models import OrganizationModel, MemberModel
from .constants import CURRENCIES, INCOME_SOURCE

"""
Features
##########
1. MonthYear Model
 - Foreign Key is Org.
 - Independent Model to summarize data from other Child models for org
 - No other Model is a direct child to this Model

2. Income Model
 - Collects Income transactions for home org members
 - Member and Org are foreign keys. Income is deleted on their deletion
 - Added signals and connector to create MonthYear entry if it doesnt exist

"""


class MonthYear(models.Model):
    """Month-Year Model for data aggregation from other models"""
    month = models.IntegerField(default=datetime.today().month,
                                choices=[(i, i) for i in range(1, 13)],
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
    primary_currency = models.CharField(default='USD',
                                        choices=CURRENCIES,
                                        max_length=3)
    is_locked = models.BooleanField(default=False,
                                    blank=False)

    # Monthly data retrieval
    # Income Model
    def income_totals(self):
        """GET MonthYear with atleast one Income/Spending data entry"""
        income = Income.objects.filter(month=self.month, year=self.year)
        total_income = 0
        total_tax_withheld = 0
        total_deductions = 0
        for entry in income:
            # 1. If Income Entry and User Primary Incomes are same currency
            if self.primary_currency == entry.currency:
                total_income += entry.income_before_tax
                total_deductions += entry.deductions
                total_tax_withheld += entry.tax_withheld

            # 2. If Income entries are in USD
            elif entry.currency == 'USD':
                conversion = from_usd_to_primary(
                    entry.income_before_tax,
                    self.primary_currency,
                    self.month, self.year,
                    self.org)
                # Check if there is a conversion object available for this month
                if conversion['result'] == 'success':
                    total_income += conversion['value']
                else:
                    print("No Currency Conversion values")
                    total_income = 0
                    break

                conversion = from_usd_to_primary(
                    entry.deductions,
                    self.primary_currency,
                    self.month, self.year,
                    self.org)
                total_deductions += conversion['value']

                conversion = from_usd_to_primary(
                    entry.tax_withheld,
                    self.primary_currency,
                    self.month,
                    self.year,
                    self.org)
                total_tax_withheld += conversion['value']

            # 3. If Month Primary Currency are in USD
            elif self.primary_currency == 'USD':
                # Convert Entry value to standard USD
                get_usd = to_usd(
                    entry.income_before_tax,
                    entry.currency,
                    self.month,
                    self.year,
                    self.org)

                if get_usd['result'] == 'success':
                    total_income += get_usd['value']
                else:
                    print("No Currency Conversion values")
                    total_income = 0
                    break

                get_usd = to_usd(
                    entry.deductions,
                    entry.currency,
                    self.month,
                    self.year,
                    self.org)
                total_deductions += get_usd['value']

                get_usd = to_usd(
                    entry.tax_withheld,
                    entry.currency,
                    self.month,
                    self.year,
                    self.org)
                total_tax_withheld += get_usd['value']

            # 4. If Income entries and primary currency are not same
            # and Monthly Primary is not USD
            else:
                # Check if there is currency object available for this month
                # Convert current value to standard USD
                get_usd = to_usd(
                    entry.income_before_tax,
                    entry.currency,
                    self.month,
                    self.year,
                    self.org)

                if get_usd['result'] == 'success':
                    get_usd = get_usd['value']
                else:
                    print("No Currency Conversion values")
                    total_income = 0
                    break

                # Convert value from USD to primary currency
                value_in_primary = from_usd_to_primary(
                    get_usd,
                    self.primary_currency,
                    self.month,
                    self.year,
                    self.org)

                if value_in_primary['result'] == 'success':
                    total_income += value_in_primary['value']
                else:
                    print("No Currency Conversion values")
                    total_income = 0
                    break

                get_usd = to_usd(
                    entry.deductions,
                    entry.currency,
                    self.month,
                    self.year,
                    self.org)
                get_usd = get_usd['value']
                value_in_primary = from_usd_to_primary(
                    get_usd,
                    self.primary_currency,
                    self.month,
                    self.year,
                    self.org)
                total_deductions += value_in_primary['value']

                get_usd = to_usd(
                    entry.tax_withheld,
                    entry.currency,
                    self.month,
                    self.year,
                    self.org)
                get_usd = get_usd['value']
                value_in_primary = from_usd_to_primary(
                    get_usd,
                    self.primary_currency,
                    self.month,
                    self.year,
                    self.org)
                total_tax_withheld += value_in_primary['value']

        response = {'total_income_before_tax': total_income,
                    'total_tax_withheld': total_tax_withheld,
                    'total_deductions': total_deductions}
        return response

    """
    # Deprecated. Added Under income_totals
    def total_tax_withheld(self):
        income = Income.objects.filter(month=self.month, year=self.year)
        total = 0
        for entry in income:
            # 1. If Income Entry and User Primary Incomes are in same currency
            if self.primary_currency == entry.currency:
                total += entry.tax_withheld

            # 2. If Income entries are in USD
            elif entry.currency == 'USD':
                conversion = from_usd_to_primary(
                    entry.tax_withheld, self.primary_currency, entry)
                if conversion['result'] == 'success':
                    total += conversion['value']
                else:
                    print("No Currency Conversion values")
                    total = 0
                    break

            # 3. If Income entries are not in USD or Monthly Primary
            else:
                # Convert current value to standard USD
                get_usd = to_usd(entry.tax_withheld, self.primary_currency, entry)
                if get_usd['result'] == 'success':
                    get_usd = get_usd['value']
                else:
                    print("No Currency Conversion values")
                    total = 0
                    break
                # Convert value from USD to primary currency
                value_in_primary = from_usd_to_primary(
                    get_usd, self.primary_currency, entry)
                if value_in_primary['result'] == 'success':
                    total += value_in_primary['value']
                else:
                    print("No Currency Conversion values")
                    total = 0
                    break
        return total

    def total_deductions(self):
        income = Income.objects.filter(month=self.month, year=self.year)
        total = 0
        for entry in income:
            # 1. If Income Entry and User Primary Incomes are in same currency
            if self.primary_currency == entry.currency:
                total += entry.deductions
            # 2. If Income entries are in USD
            elif entry.currency == 'USD':
                conversion = from_usd_to_primary(
                    entry.deductions, self.primary_currency, entry)
                if conversion['result'] == 'success':
                    total += conversion['value']
                else:
                    print("No Currency Conversion values")
                    total = 0
                    break
            # 3. If Income entries are not in USD or Monthly Primary
            else:
                # Convert current value to standard USD
                get_usd = to_usd(entry.deductions, self.primary_currency, entry)
                if get_usd['result'] == 'success':
                    get_usd = get_usd['value']
                else:
                    print("No Currency Conversion values")
                    total = 0
                    break
                # Convert value from USD to primary currency
                value_in_primary = from_usd_to_primary(
                    get_usd, self.primary_currency, entry)
                if value_in_primary['result'] == 'success':
                    total += value_in_primary['value']
                else:
                    print("No Currency Conversion values")
                    total = 0
                    break

        return total
    """
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
    income_before_tax = models.FloatField(blank=False)
    tax_withheld = models.FloatField(default=0.0, blank=False)
    deductions = models.FloatField(default=0.0, blank=False)
    currency = models.CharField(default='INR',
                                choices=CURRENCIES,
                                max_length=3)
    last_updated_on = models.DateField(auto_now_add=True)
    income_date = models.DateField(default=datetime.today().date, blank=False)
    month = models.IntegerField(default=datetime.today().month,
                                choices=[(i, i) for i in range(1, 13)],
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
    org = models.ForeignKey(OrganizationModel,
                            on_delete=models.CASCADE, )
    member = models.ForeignKey(MemberModel,
                               on_delete=models.CASCADE, )

    class Meta:
        index_together = ('member', 'org', 'month', 'year')


#################
# Backend models
##################
class CurrencyConverter(models.Model):
    """Currency conversion database """
    currency = models.CharField(choices=CURRENCIES, max_length=3, blank=False)
    # Value of one USD in the currency listed above
    one_dollar_in_currency = models.FloatField(blank=False,
                                               validators=[
                                                   MinValueValidator(0)
                                               ])
    month = models.IntegerField(default=datetime.today().month,
                                choices=[(i, i) for i in range(1, 13)],
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
    org = models.ForeignKey(OrganizationModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('currency', 'month', 'year')
        index_together = ('currency', 'month', 'year')


##########################
# Currency Related methods
##########################
def to_usd(value, from_currency, month, year, org):
    """Convert from any currency to USD"""
    try:
        currency_converter = CurrencyConverter.objects.get(
            currency=from_currency, month=month, year=year, org=org)
        value_in_usd = value / currency_converter.one_dollar_in_currency
        # print(value,"(", from_currency, ") = " , value_in_usd, "(USD)" )
        return {'result': 'success', 'value': value_in_usd}
    except Exception as e:
        return {'result': 'error', 'value': e}


def from_usd_to_primary(value, to_currency, month, year, org):
    """Convert from USD to required currency"""
    try:
        currency_converter = CurrencyConverter.objects.get(
            currency=to_currency, month=month, year=year, org=org)
        value_in_primary = value * currency_converter.one_dollar_in_currency
        # print(value, "(USD) = " , value_in_primary,"(", to_currency, ") " )
        return {'result': 'success', 'value': value_in_primary}
    except Exception as e:
        return {'result': 'error', 'value': e}
