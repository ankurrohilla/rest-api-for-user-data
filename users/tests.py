# Create your tests here.
import json

import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User
from .serializers import UserSerializer


class UserTests(APITestCase):

    def setUp(self):
        james = {
            "id": 1,
            "first_name": "James",
            "last_name": "Butt",
            "company_name": "Benton, John B Jr",
            "city": "New Orleans",
            "state": "LA",
            "zip": "70116",
            "email": "jbutt@gmail.com",
            "web": "http://www.bentonjohnbjr.com",
            "age": 70
        }
        ryan = {
            "id": 2,
            "first_name": "Ryan",
            "last_name": "Butt",
            "company_name": "Benton, John B Jr",
            "city": "New Orleans",
            "state": "LA",
            "zip": "70116",
            "email": "rbutt@gmail.com",
            "web": "http://www.bentonjohnbjr.com",
            "age": 50
        }
        self.valid_payload = {
            "id": 3,
            "first_name": "Nick",
            "last_name": "Butt",
            "company_name": "Benton, John B Jr",
            "city": "New Orleans",
            "state": "LA",
            "zip": "70116",
            "email": "nbutt@gmail.com",
            "web": "http://www.bentonjohnbjr.com",
            "age": 50
        }
        self.invalid_payload = {
            'name': 'ar',
            'age': 4,
        }
        self.james = User.objects.create(**james)
        self.ryan = User.objects.create(**ryan)

    def test_get_all_users(self):
        # get API response
        response = self.client.get(reverse('api:users:user-list'))
        # get data from db
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ordering_valid(self):
        for f in User._meta.fields:
            url1 = f"{reverse('api:users:user-list')}?sort={f.name}"
            url2 = f"{reverse('api:users:user-list')}?sort=-{f.name}"
            response = self.client.get(url1)
            response2 = self.client.get(url2)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_ordering_invalid(self):
        url = '%s?sort=abc' % (reverse('api:users:user-list'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_valid_single_user(self):
        response = self.client.get(
            reverse('api:users:user-detail', kwargs={'id': self.ryan.id}))
        user = User.objects.get(pk=self.ryan.pk)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_user(self):
        response = self.client.get(
            reverse('api:users:user-detail', kwargs={'id': 7390}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_user(self):
        """
               Ensure we can create a new user object.
        """
        url = reverse('api:users:user-list')
        assert url == '/api/users/'
        response = self.client.post(
            url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        url = reverse('api:users:user-list')
        response = self.client.post(
            url,
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_user(self):
        url = reverse('api:users:user-detail', kwargs={'id': self.james.id})
        response = self.client.put(
            url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_user(self):
        url = reverse('api:users:user-detail', kwargs={'id': self.james.id})
        response = self.client.put(
            url,
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_user(self):
        url = reverse('api:users:user-detail', kwargs={'id': self.james.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_user(self):
        url = reverse('api:users:user-detail', kwargs={'id': 90})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserLimitTest(APITestCase):
    def setUp(self) -> None:
        self.URL = 'https://datapeace-storage.s3-us-west-2.amazonaws.com/dummy_data/users.json'
        r = requests.get(self.URL)
        self.users = [User(**u) for u in r.json()]
        self.users_list = User.objects.bulk_create(self.users)

    def test_limit_valid(self):
        url1 = reverse('api:users:user-list')
        url2 = '%s?limit=20' % (reverse('api:users:user-list'))
        response1 = self.client.get(url1)
        response2 = self.client.get(url2)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 5)  # default limit test
        self.assertEqual(len(response2.data), 20)
