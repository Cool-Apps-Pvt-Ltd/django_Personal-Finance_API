from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from personal_finance_api import serializers, models, permissions


class UserProfileViewSet(viewsets.ModelViewSet):
    """User Profile GET/POST/DELETE/PUT/PATCH API"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('last_name', 'email')


class LoginApiView(ObtainAuthToken):
    """User Login and handle Token creation"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    

