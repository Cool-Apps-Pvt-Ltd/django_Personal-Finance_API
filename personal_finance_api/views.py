from rest_framework import viewsets, filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.settings import api_settings
from .serializers import UserProfileSerializer
from personal_finance_api import serializers, permissions
from .models import UserProfile, OrganizationModel, MemberModel

"""
READY and TESTED
###############################################
1. UserProfileViewSet
- Superusers can GET/PUT/PATCH any Profile
- Regular Users only GET/PUT/PATCH/POST/DELETE their own profile
- Permissions for superuser and regular user tested

2. LoginApiVIew

3. OrganizationViewSet
- Superusers can GET/PUT/PATCH any Org
- Authenticated users can GET/POST/PUT/PATCH/DELETE own Org
- Permissions for superuser and regular user tested

4. MemberViewSet
- Superusers can GET/PUT/PATCH any Org Members
- Authenticated users can GET/POST/PUT/PATCH/DELETE own Org
- "Family" user cannot be DELETED
- Permissions for superuser and regular user tested

"""


class UserProfileViewSet(viewsets.ModelViewSet):
    """User Profile GET/POST/DELETE/PUT/PATCH API"""
    serializer_class = serializers.UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('last_name', 'email')

    def get_queryset(self):
        # Superuser gets all users
        if self.request.user.is_superuser:
            return super().get_queryset()

        # Show user's own profile only
        return super().get_queryset().filter(id=self.request.user.id)


@api_view(['POST'])
def create_user(request, *args, **kwargs):
    if 'email' in request.data and \
            'password' in request.data and \
            'last_name' in request.data and \
            'first_name' in request.data:
        try:
            user = UserProfile()
            user.email = request.data['email']
            user.set_password(request.data['password'])
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.save()

            serializer = UserProfileSerializer(user, many=False)
            response = {'message': 'User Created', 'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {'Error': str(e)}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    else:
        response = {'message': 'Invalid Request'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(ObtainAuthToken):
    """User Login and handle Token creation"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class OrganizationViewSet(viewsets.ModelViewSet):
    """Organization creation and handling"""
    serializer_class = serializers.OrganizationSerializer
    queryset = OrganizationModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.HomeOrgUpdate,)

    def get_queryset(self):
        """Get subset of Orgs for logged in user"""
        # Superuser gets all Orgs
        if self.request.user.is_superuser:
            return super().get_queryset()

        if self.request.user.is_authenticated:
            return super().get_queryset().filter(user=self.request.user)
        else:
            return super().queryset

    def perform_create(self, serializer):
        """Override Org Creation to add user info"""
        serializer.save(user=self.request.user)


class MemberViewSet(viewsets.ModelViewSet):
    """Member creation and handling"""
    serializer_class = serializers.MemberSerializer
    queryset = MemberModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.OrgElementPermissions,)

    def get_queryset(self):
        """GET members in an org"""
        return super().get_queryset().filter(org=self.kwargs['org_id'])

    def perform_create(self, serializer):
        """Override Member POST to add org info"""
        try:
            org = OrganizationModel.objects.get(id=self.kwargs['org_id'])
            serializer.save(org=org)
        except Exception as e:
            return super().permission_denied(self.request, e)

    def partial_update(self, request, *args, **kwargs):
        """Check Member name 'Family' and run PATCH"""
        try:
            member = MemberModel.objects.get(id=kwargs['pk'])
            if member.is_deleted:
                response = {
                    'Message': 'CAN\'T modify deleted member: ' + member.name
                }
                return Response(response,
                                status=status.HTTP_403_FORBIDDEN)
            else:
                # Cannot edit Member family
                if member.name != 'Family':
                    return super().partial_update(request, *args, **kwargs)
                else:
                    response = {
                        'Message': 'CAN\'T modify member \'Family\''
                    }
                    super().permission_denied(self.request, response)

        except Exception as e:
            return super().permission_denied(self.request, e)

    def update(self, request, *args, **kwargs):
        """Check Member name 'Family' and run PUT"""
        try:
            member = MemberModel.objects.get(id=kwargs['pk'])
            if member.is_deleted:
                response = {
                    'Message': 'CAN\'T modify deleted member: ' + member.name
                }
                return Response(response,
                                status=status.HTTP_403_FORBIDDEN)
            else:
                # Cannot edit Member 'family'
                if member.name != 'Family':
                    return super().update(request, *args, **kwargs)
                else:
                    response = {
                        'Message': 'CAN\'T update member \'Family\''
                    }
                    super().permission_denied(self.request, response)
        except Exception as e:
            return super().permission_denied(self.request, e)

    def destroy(self, request, *args, **kwargs):
        """Check Member name 'Family' and run DELETE"""
        try:
            member = MemberModel.objects.get(id=kwargs['pk'])
            if member.is_deleted:
                response = {
                    'Message': 'CAN\'T modify deleted member: ' + member.name
                }
                return Response(response,
                                status=status.HTTP_403_FORBIDDEN)
            else:
                # Cannot DELETE Member family
                if member.name != 'Family':
                    member.is_deleted = True
                    member.save()
                    response = {
                        'Message': 'Deleted: ' + member.name
                    }
                    return Response(response,
                                    status=status.HTTP_200_OK)
                else:
                    response = {
                        'Message': 'CAN\'T delete member \'Family\''
                    }
                    super().permission_denied(self.request, response)

        except Exception as e:
            return super().permission_denied(self.request, e)
