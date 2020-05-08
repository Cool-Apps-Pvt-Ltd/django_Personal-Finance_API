from rest_framework import serializers
from personal_finance_api import models


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes User Profile Object"""
    class Meta:
        model = models.UserProfile
        fields = ('id', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True,
                         'style': {'input_type': 'password'}
                         }
        }

    def create(self, validated_data):
        """Create and return a new user.
        Overrides Create function for this serializer"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )

        return user


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializes Home Organization Container Object"""
    class Meta:
        model = models.OrganizationModel
        fields = ('id', 'home_name', 'license_state',
                  'license_expiry', 'dashboard_currency', 'user')
        extra_kwargs = {
            'user': {'read_only': True, },
            'license_state': {'read_only': True, },
            'license_expiry': {'read_only': True, },
        }


class MemberSerializer(serializers.ModelSerializer):
    """Serializes Members in an Org"""
    class Meta:
        model = models.MemberModel
        fields = ('id', 'name', 'org', )
        extra_kwargs = {
            'org': {'read_only': True, },
        }
