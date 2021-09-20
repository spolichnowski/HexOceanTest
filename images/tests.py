from rest_framework import status
import json
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from .models import ImageAPI, CustomImageSize
from profiles.models import Profile
from io import BytesIO
from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


class BasicTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='TestUsername', password='BasiCUser2')
        self.profile = Profile.objects.create(user=self.user, tier='BASIC')
        self.token = Token.objects.get(user=self.user)
        self.authentication()

        bts = BytesIO()
        img = Image.new("RGB", (800, 1100))
        img.save(bts, 'jpeg')
        temp_image = SimpleUploadedFile('test_image.jpg', bts.getvalue())
        ImageAPI.objects.create(owner=self.user, image=temp_image)

    def authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_images(self):
        url = reverse('images')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_images_elements(self):
        url = reverse('images')
        response = self.client.get(url, format='json')
        keys = list(response.data[0].keys())
        self.assertEqual(keys, ['thumbnail_200'])

    def test_post_image(self):
        url = reverse('images')
        bts = BytesIO()
        img = Image.new("RGB", (800, 1100))
        img.save(bts, 'jpeg')
        temp_image = SimpleUploadedFile('test_image.jpg', bts.getvalue())

        body = {
            "image": temp_image
        }
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PremiumTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='TestUsernamePremium', password='PremiuMUser2')
        self.profile = Profile.objects.create(user=self.user, tier='PREMIUM')
        self.token = Token.objects.get(user=self.user)
        self.authentication()
        bts = BytesIO()
        img = Image.new("RGB", (800, 1100))
        img.save(bts, 'jpeg')
        temp_image = SimpleUploadedFile('test_image.jpg', bts.getvalue())
        ImageAPI.objects.create(owner=self.user, image=temp_image)

    def authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_images_elements(self):
        url = reverse('images')
        response = self.client.get(url, format='json')
        keys = list(response.data[0].keys())
        self.assertEqual(keys, ['image', 'thumbnail_200', 'thumbnail_400'])


class EnterpriseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='TestUsernameEnterprise', password='EnterprisEUser2')
        self.profile = Profile.objects.create(
            user=self.user, tier='ENTERPRISE')
        self.token = Token.objects.get(user=self.user)
        self.authentication()
        bts = BytesIO()
        img = Image.new("RGB", (800, 1100))
        img.save(bts, 'jpeg')
        temp_image = SimpleUploadedFile('test_image.jpg', bts.getvalue())
        ImageAPI.objects.create(owner=self.user, image=temp_image)

    def authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_images_elements(self):
        url = reverse('images')
        response = self.client.get(url, format='json')
        keys = list(response.data[0].keys())
        self.assertEqual(keys, ['image', 'thumbnail_200', 'thumbnail_400'])


class CustomTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='TestUsernameCustom', password='CustoMUser2')
        self.profile = Profile.objects.create(user=self.user, tier='CUSTOM')
        self.token = Token.objects.get(user=self.user)
        self.authentication()

        bts = BytesIO()
        img = Image.new("RGB", (800, 1100))
        img.save(bts, 'jpeg')
        temp_image = SimpleUploadedFile('test_image.jpg', bts.getvalue())
        image = ImageAPI.objects.create(owner=self.user, image=temp_image)
        CustomImageSize.objects.create(image_api=image, custom_height=172)

    def authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_images(self):
        url = reverse('images')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_images_elements(self):
        url = reverse('images')
        response = self.client.get(url, format='json')
        keys = list(response.data[0].keys())
        self.assertEqual(keys, ['image', 'thumbnail_200',
                                'thumbnail_400', 'custom_thumbnails'])
