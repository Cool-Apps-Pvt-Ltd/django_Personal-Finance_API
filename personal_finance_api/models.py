from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .constants import CURRENCIES, ORG_LICENSE_STATE


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, first_name, last_name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Email Address is mandatory')

        email = self.normalize_email(email) # Normalize the emails to correct formatting
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """Create a new SUPER user profile"""
        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True # Automatically created by PermissionsMixin in the UserProfile Class
        user.is_staff = True
        user.save(using=self._db)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database Model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_name(self):
        """Retrieve Name of the user"""
        response = {'first_name' : self.first_name, 'last_name': self.last_name}
        return response

    def get_full_name(self):
        """Retrieve Fullname of the user"""
        response = str(self.first_name + str(' ') + self.last_name)
        return response

    def get_short_name(self):
        """Retrieve Nickname of the user"""
        return self.first_name

    def __str__(self):
        """Return string representation of the user"""
        return self.email


class OrganizationModel(models.Model):
    """Organization Container to have finance details of a family"""
    home_name = models.CharField(default='My Home', max_length=20,)
    license_state = models.CharField(default='L', choices=ORG_LICENSE_STATE, blank=False, max_length=1)
    license_expiry = models.DateField(blank=False, default='2024-12-12')
    dashboard_currency = models.CharField(default='INR', choices=CURRENCIES, max_length=3)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, )


class MemberModel(models.Model):
    """Members of the home org"""
    name = models.CharField(max_length=10, blank=False, default="Family" )
    org = models.ForeignKey(OrganizationModel, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('org', 'name',))
        index_together = (('org', 'name',))