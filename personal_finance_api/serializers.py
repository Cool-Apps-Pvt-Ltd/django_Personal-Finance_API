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
                  'license_expiry', 'dashboard_currency', 'user',
                  'created_on', 'is_deleted', 'is_shutdown')
        extra_kwargs = {
            'user': {'read_only': True, },
            'license_state': {'read_only': True, },
            'license_expiry': {'read_only': True, },
            'created_on': {'read_only': True, },
            'is_deleted': {'read_only': True, },
            'is_shutdown': {'read_only': True, },
        }


class MemberSerializer(serializers.ModelSerializer):
    """Serializes Members in an Org"""
    class Meta:
        model = models.MemberModel
        fields = ('id', 'name', 'org',
                  'last_updated_on', 'created_on',
                  'is_deleted')
        extra_kwargs = {
            'org': {'read_only': True, },
            'created_on': {'read_only': True, },
            'is_deleted': {'read_only': True, },
            'last_updated_on': {'read_only': True, },
        }
