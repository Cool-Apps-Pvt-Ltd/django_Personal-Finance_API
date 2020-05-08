from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user(self):
        """Test creating a new user with email and password"""
        email = 'test@email.com'
        password = 'password123'
        first_name = 'First Name'
        last_name = 'Last Name'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)

    def test_create_user_email_normalized(self):
        """Test for Normalized email @ new user creation"""
        email = 'test@EMAIL.COM'
        password = 'password123'
        first_name = 'First Name'
        last_name = 'Last Name'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating new user with no email raises error"""
        password = 'password123'
        first_name = 'First Name'
        last_name = 'Last Name'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

    def test_create_superuser(self):
        """Test Creating super user using commandline"""
        email = 'test@email.com'
        password = 'password123'
        first_name = 'First Name'
        last_name = 'Last Name'
        super_user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.super_user.is_staff)
