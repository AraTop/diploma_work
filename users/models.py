from django.db import models
from django.contrib.auth.models import AbstractUser
from main.models import Сhannel
from users.validators import valid_number, valid_number_2

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=11, verbose_name='Номер телефона без +', unique=True, validators=[valid_number, valid_number_2])
    email = models.EmailField(unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', **NULLABLE)
    surname = models.CharField(max_length=200, verbose_name='Отчествоо', **NULLABLE)
    nickname = models.CharField(max_length=10, verbose_name='Имя, которое видно всем', unique=True, **NULLABLE)
    balance = models.FloatField(verbose_name='Баланс', **NULLABLE, default=0)
    profile_icon = models.ImageField(upload_to='users/', verbose_name='Фотография профиля', **NULLABLE)
    description = models.TextField(verbose_name='Описание профиля', **NULLABLE)
    channel = models.ForeignKey(Сhannel, on_delete=models.SET_NULL, **NULLABLE)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = [email]
