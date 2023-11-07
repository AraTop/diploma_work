from django.db import models
from django.contrib.auth.models import AbstractUser
from main.models import Сhannel

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', **NULLABLE)
    surname = models.CharField(max_length=200, verbose_name='Отчествоо', **NULLABLE)
    nickname = models.CharField(max_length=10, verbose_name='Имя, которое видно всем', unique=True)
    balance = models.IntegerField(verbose_name='Баланс', **NULLABLE)
    profile_icon = models.ImageField(upload_to='users/', verbose_name='Фотография профиля', **NULLABLE)
    description = models.TextField(verbose_name='Описание профиля', default='test', **NULLABLE)
    channel = models.ForeignKey(Сhannel, on_delete=models.CASCADE, **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    