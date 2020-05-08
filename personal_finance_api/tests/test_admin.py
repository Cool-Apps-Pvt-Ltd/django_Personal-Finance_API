from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@email.com",
            password="password123",
            first_name="First Name",
            last_name="Last Name"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test@email.com",
            password="password123",
            first_name="First Name",
            last_name="Last Name"
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:personal_finance_api_userprofile_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)

    def test_user_change_page(self):
        """Test that user edit page works"""
        url = reverse('admin:personal_finance_api_userprofile_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
