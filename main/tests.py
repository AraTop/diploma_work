from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from .models import Post, Subscriptions, Сhannel, Сomments
from rest_framework.test import APIClient
from django.utils import timezone


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
            'description': 'test'
        }
        response = self.client.post(reverse('main:create_channel'), data=new_channel_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.assertRedirects(response, reverse('main:detail', args=['test']))

    def test_read_channel(self):
        new_channel_data = {
            'name': 'test',
            'description': 'test'
        }
        response = self.client.post(reverse('main:create_channel'), data=new_channel_data)

        response = self.client.get(reverse('main:detail', args=['test']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_channel(self):
        new_channel_data = {
            'name': 'test',
            'description': 'test'
        }
        response = self.client.post(reverse('main:create_channel'), data=new_channel_data)

        updated_channel_data = {
            'name': 'test1',
            'description': 'test1'
        }
        channel = Сhannel.objects.get(name='test')
        response = self.client.put(reverse('main:update_channel', args=[channel.id]), data=updated_channel_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriptionsCRUDTestCase(APITestCase):

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

    def test_create_subscription(self):
        new_channel_data = {
            'name': 'test',
            'description': 'test'
        }
        response = self.client.post(reverse('main:create_channel'), data=new_channel_data)
        channel = Сhannel.objects.get(name='test')

        new_subscription_data = {
            'name': 'test',
            'description': 'test',
            'strength_of_subscription': 1,
            'amount_per_month': 100,
            'channel': channel.pk
        }
        response = self.client.post(reverse('main:create_sub'), data=new_subscription_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_read_subscription(self):
        new_channel_data = {
            'name': 'test',
            'description': 'test'
        }
        response = self.client.post(reverse('main:create_channel'), data=new_channel_data)
        channel = Сhannel.objects.get(name='test')

        new_subscription_data = {
            'name': 'test',
            'description': 'test',
            'strength_of_subscription': 1,
            'amount_per_month': 100,
            'channel': channel.pk
        }
        response = self.client.post(reverse('main:create_sub'), data=new_subscription_data)
        subscrip = Subscriptions.objects.get(name='test')

        response = self.client.get(reverse('main:detail_sub', args=[subscrip.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_subscription(self):
        new_channel_data = {
            'name': 'test',
            'description': 'test'
        }
        response = self.client.post(reverse('main:create_channel'), data=new_channel_data)
        channel = Сhannel.objects.get(name='test')

        new_subscription_data = {
            'name': 'test',
            'description': 'test',
            'strength_of_subscription': 1,
            'amount_per_month': 100,
            'channel': channel.pk
        }
        response = self.client.post(reverse('main:create_sub'), data=new_subscription_data)

        updated_subscription_data = {
            'name': 'test1',
            'description': 'test1',
            'strength_of_subscription': 1,
            'amount_per_month': 100,
            'channel': channel.pk
        }
        subscription = Subscriptions.objects.get(name='test')
        response = self.client.put(reverse('main:update_sub', args=[subscription.id]), data=updated_subscription_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostCRUDTestCase(APITestCase):

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

    def test_create_post(self):
        new_channel_data = {
            'name': 'test',
            'description': 'test'
        }
        response = self.client.post(reverse('main:create_channel'), data=new_channel_data)
        channel = Сhannel.objects.get(name='test')

        new_post_data = {
            'name': 'test',
            'time_the_comment': timezone.now(),
            'channel': channel.pk
        }
        response = self.client.post(reverse('main:create_post'), data=new_post_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_update_post(self):
        new_channel_data = {
            'name': 'test',
            'description': 'test'
        }
        response = self.client.post(reverse('main:create_channel'), data=new_channel_data)
        channel = Сhannel.objects.get(name='test')

        new_post_data = {
            'name': 'test',
            'time_the_comment': timezone.now(),
            'channel': channel.pk
        }
        response = self.client.post(reverse('main:create_post'), data=new_post_data)

        new_update_post_data = {
            'name': 'test1',
            'time_the_comment': timezone.now(),
            'channel': channel.pk
        }
        post = Post.objects.get(name='test')
        response = self.client.put(reverse('main:update_post', args=[post.id]), data=new_update_post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class СommentsCRUDTestCase(APITestCase):

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

    def test_create_comments(self):
        new_channel_data = {
            'name': 'test',
            'description': 'test'
        }
        response = self.client.post(reverse('main:create_channel'), data=new_channel_data)
        channel = Сhannel.objects.get(name='test')

        new_post_data = {
            'name': 'test',
            'time_the_comment': timezone.now(),
            'channel': channel.pk
        }
        response = self.client.post(reverse('main:create_post'), data=new_post_data)
        post = Post.objects.get(name='test')

        new_comments_data = {
            'user': 'test',
            'description': 'test',
            'time_the_comment': timezone.now(),
            'post': post.pk
        }
        url = reverse('main:create_comm', kwargs={'post_id': post.id})
        response = self.client.post(url, data=new_comments_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_update_comments(self):
        new_channel_data = {
            'name': 'test',
            'description': 'test'
        }
        response = self.client.post(reverse('main:create_channel'), data=new_channel_data)
        channel = Сhannel.objects.get(name='test')

        new_post_data = {
            'name': 'test',
            'time_the_comment': timezone.now(),
            'channel': channel.pk
        }
        response = self.client.post(reverse('main:create_post'), data=new_post_data)
        post = Post.objects.get(name='test')

        new_comments_data = {
            'user': 'test',
            'description': 'test',
            'time_the_comment': timezone.now(),
            'post': post.pk
        }
        url = reverse('main:create_comm', kwargs={'post_id': post.id})
        response = self.client.post(url, data=new_comments_data)
        comm = Сomments.objects.get(user='test')

        new_update_comment_data = {
            'user': 'test1',
            'description': 'test1',
            'time_the_comment': timezone.now(),
            'post': post.pk
        }
        url = reverse('main:update_comm', kwargs={'pk': comm.id})
        response = self.client.post(url, data=new_update_comment_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
