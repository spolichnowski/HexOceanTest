from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from profiles.models import Profile
from django.urls import reverse
from django.contrib.auth.models import User


class ProfileTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='TestUsername', password='BasiCUser2')
        self.profile = Profile.objects.create(user=self.user, tier='BASIC')
        self.token = Token.objects.get(user=self.user)
        self.authentication()

    def authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_images_authenticated(self):
        url = reverse('images')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_images_un_authenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('images')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
