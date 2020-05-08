from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .models import UserProfile, OrganizationModel, MemberModel
from personal_finance_api import serializers, permissions


class UserProfileViewSet(viewsets.ModelViewSet):
    """User Profile GET/POST/DELETE/PUT/PATCH API"""
    serializer_class = serializers.UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('last_name', 'email')


class LoginApiView(ObtainAuthToken):
    """User Login and handle Token creation"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class OrganizationViewSet(viewsets.ModelViewSet):
    """Organization creation and handling"""
    serializer_class = serializers.OrganizationSerializer
    queryset = OrganizationModel.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.HomeOrgUpdate, )

    def get_queryset(self):
        """Get subset of Orgs for logged in user"""
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        """Override Org Creation to add user info"""
        serializer.save(user=self.request.user)


class MemberViewSet(viewsets.ModelViewSet):
    """Member creation and handling"""
    serializer_class = serializers.MemberSerializer
    queryset = MemberModel.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.HomeOrgUpdate, )

    def get_queryset(self):
        return super().get_queryset().filter(org=self.request.org)
