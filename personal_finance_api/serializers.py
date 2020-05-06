from rest_framework import serializers


class UserProfileSerializer(serializers.Serializer):
    """Serializes Name fields for User Profile"""
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
