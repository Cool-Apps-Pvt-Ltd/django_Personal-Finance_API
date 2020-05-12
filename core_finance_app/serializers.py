from rest_framework import serializers
from .models import Income, MonthYear, CurrencyConverter


class MonthYearSerializer(serializers.ModelSerializer):
    """Serializer MonthYear Model data"""
    class Meta:
        model = MonthYear
        fields = ('id', 'month', 'year',
                  'is_locked', 'org',
                  'income_totals',
                  'primary_currency',)
        extra_kwargs = {
            'id': {'read_only': True, },
            'org': {'read_only': True, },
            'income_totals': {'read_only': True, },
         }


class IncomeSerializer(serializers.ModelSerializer):
    """Serializer Income Model data"""
    class Meta:
        model = Income
        fields = ('id', 'income_source', 'income_before_tax',
                  'tax_withheld', 'deductions', 'currency',
                  'last_updated_on', 'income_date', 'month', 'year',
                  'member', 'org',
                  )
        extra_kwargs = {
            'last_updated_on': {'read_only': True},
            'org': {
                'read_only': True,
            },
        }


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer MonthYear Model data"""
    class Meta:
        model = CurrencyConverter
        fields = ('id', 'currency',
                  'one_dollar_in_currency', 'org',
                  'month', 'year',)
        extra_kwargs = {
            'org': {'read_only': True, },
         }
