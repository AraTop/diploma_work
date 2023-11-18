from django.db import models
from django.contrib.auth.models import AbstractUser
from main.models import Сhannel

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=13, verbose_name='Номер телефона', unique=True)
    email = models.EmailField(unique=True, verbose_name='Почта', **NULLABLE)
    first_name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', **NULLABLE)
    surname = models.CharField(max_length=200, verbose_name='Отчествоо', **NULLABLE)
    nickname = models.CharField(max_length=10, verbose_name='Имя, которое видно всем', unique=True)
    balance = models.FloatField(verbose_name='Баланс', **NULLABLE, default=0)
    profile_icon = models.ImageField(upload_to='users/', verbose_name='Фотография профиля', **NULLABLE)
    description = models.TextField(verbose_name='Описание профиля', default='test', **NULLABLE)
    channel = models.ForeignKey(Сhannel, on_delete=models.SET_NULL, **NULLABLE)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    