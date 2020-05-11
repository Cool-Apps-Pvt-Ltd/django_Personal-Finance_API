from rest_framework import serializers
from .models import Income


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
            'last_updated_on': {'read_only': True}
        }

    def create(self, validated_data):
        """Create and return a new Income Transaction.
        Overrides Create function for this serializer"""
        print("Income Serializer - Create")
        pass
