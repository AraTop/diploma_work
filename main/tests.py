import datetime
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from .models import Сhannel
from rest_framework.test import APIClient


class ChannelCRUDTestCase(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            phone_number='79781072923',
            is_superuser=True,
            is_staff=True,
            is_active=True
                )
        self.user.set_password('12345')
        self.user.save()
        self.client.login(phone_number='79781072923', password='12345')

    def test_create_channel(self):
        new_channel_data = {
            'name': 'test',
            'description': 'test',
            'profile_icon': None
        }
        response = self.client.post(reverse('main:create_channel'), data=new_channel_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_channel(self):
        response = self.client.get(reverse('main:detail', args=['test']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_channel(self):
        updated_channel_data = {
            'name': 'test1',
            'description': 'test1',
            'profile_icon': None
        }
        channel = Сhannel.objects.get(name='test1')
        response = self.client.put(reverse('main:update_channel', args=[channel.id]), data=updated_channel_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
