from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow Users to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check if the user is trying to edit their own profile"""
        # Allow Users to GET all profiles
        if request.method in permissions.SAFE_METHODS:
            return True

        # If method is not in SAFE_METHODS
        # Returns True if updating their own profile
        return obj.id == request.user.id

