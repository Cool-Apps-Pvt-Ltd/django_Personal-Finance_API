from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from personal_finance_api import serializers, models, permissions


class UserProfileView(APIView):
    """User Profile GET/POST/DELETE/PUT/PATCH API"""
    serializer_class = serializers.UserProfileSerializer

    def get(self, request):
        """User Profile GET API"""
        response = {'message': 'Test UserProfileView'}
        return Response(response, status.HTTP_200_OK)

    def post(self, request):
        """User Profile POST API"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():                 #validate Serializer
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            response = {'message': {'first_name' : first_name, 'last_name': last_name}}
            return Response(response, status.HTTP_200_OK)

        else:
            response = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """User Profile PUT API - Updates complete profile"""
        response = {'message': 'put'}
        return Response(response, status.HTTP_200_OK)

    def patch(self, request, pk=None):
        """User Profile PATCH API - Updates only entered fields in profile"""
        response = {'message': 'patch'}
        return Response(response, status.HTTP_200_OK)

    def delete(self, request, pk=None):
        """User Profile DELETE API - Updates only entered fields in profile"""
        response = {'message': 'delete'}
        return Response(response, status.HTTP_200_OK)

class UserProfileViewSet(viewsets.ModelViewSet):
    """User Profile GET/POST/DELETE/PUT/PATCH API"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile, )

