from rest_framework import permissions
from .models import OrganizationModel, UserProfile


class UpdateOwnProfile(permissions.BasePermission):
    """Allow Users to edit their own profile"""

    def has_permission(self, request, view):
        """Check if the user is trying to access their own profile"""
        # POST doesn't need user to be authenticated
        if request.method in ['GET', 'PUT', 'PATCH']:
            # Allow Superusers to access GET/PUT/PATCH User Profile
            if request.user.is_staff or request.user.is_superuser:
                return True
            # Allow Users to GET/PUT/PATCH Userprofile
            return request.user.is_authenticated

        elif request.method in ['DELETE']:
            # DENY Superusers to DELETE Userprofile
            if request.user.is_staff or request.user.is_superuser:
                return False
            # Allow Users to DELETE Userprofile
            return request.user.is_authenticated


class HomeOrgUpdate(permissions.BasePermission):
    """Allow Users to edit their own Home Orgs"""

    def has_permission(self, request, view):
        """Check if the user is trying to edit their own org"""
        if request.method in ['GET', 'PUT', 'PATCH']:
            # Allow Superusers to access GET/PUT/PATCH orgs
            if request.user.is_staff or request.user.is_superuser:
                return True
            # Allow Users to GET/PUT/PATCH Home Org Details
            return request.user.is_authenticated

        elif request.method in ['DELETE', 'POST']:
            # DENY Superusers to DELETE/POST orgs
            if request.user.is_staff or request.user.is_superuser:
                return False
            # Allow Users to DELETE/POST Home Org Details
            return request.user.is_authenticated


class OrgMemberUpdate(permissions.BasePermission):
    """
        Return Permissions for Superuser/admin/org
        owner to edit home elements
    """
    def has_permission(self, request, view):
        try:
            # Get Requested User's Details
            requester_user_id = request.user.id
            requester = UserProfile.objects.get(id=request.user.id)
            requester_is_superuser = requester.is_superuser
            requester_is_staff = requester.is_staff
            requester_is_active = requester.is_active

            # Get User details from the Org in the URL
            org = OrganizationModel.objects.get(id=view.kwargs['org_id'])
            org_user = UserProfile.objects.get(id=org.user.id)
            org_user_id = org_user.id

            if request.method in ['GET', 'PUT', 'PATCH']:
                # Allow Users to GET/PUT/PATCH Home Org elements
                if request.user.is_authenticated and \
                        requester_user_id == org_user_id and requester_is_active:
                    return True
                # Allow Superusers to access GET/PUT/PATCH org elements
                if requester_is_superuser or requester_is_staff:
                    return True
                return False

            if request.method in ['DELETE', 'POST']:
                # Allow Users to DELETE/POST Home Org elements
                if request.user.is_authenticated and \
                        requester_user_id == org_user_id and requester_is_active:
                    return True
                # DENY Superusers to DELETE/POST Org elements
                return False
        except:
            return False
