from rest_framework import serializers
from .models import Income


class MonthYearSerializer(serializers.ModelSerializer):
    """Serializer MonthYear Model data"""
    class Meta:
        model = Income
        fields = ('id', 'month', 'year',
                  'is_locked', 'org',
                  'primary_currency',)
        extra_kwargs = {
            'org': {
                'read_only': True,
            },
        }


class IncomeSerializer(serializers.ModelSerializer):
    """Serializer Income Model data"""
    class Meta:
        model = Income
        fields = ('id', 'income_source', 'income_before_tax',
                  'tax_withheld', 'deductions', 'currency',
                  'last_updated_on', 'month', 'year',
                  'member', 'org',
                  )
        extra_kwargs = {
            'last_updated_on': {'read_only': True},
            'org': {
                'read_only': True,
            },
        }
