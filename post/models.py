from django.db import models
from main.models import Сhannel
from subscription.models import Subscriptions

NULLABLE = {'null': True, 'blank': True}


class Post(models.Model):
    name = models.CharField(max_length=70, verbose_name='Название поста')
    photo_post = models.ImageField(upload_to='post/', verbose_name='фотография к посту', **NULLABLE)
    description = models.TextField(verbose_name='Описание поста', **NULLABLE)
    subscription_level = models.ForeignKey(Subscriptions, on_delete=models.SET_NULL, **NULLABLE)
    likes = models.IntegerField(verbose_name='Кол-во лайков', **NULLABLE, default=0)
    time_the_comment = models.DateTimeField(verbose_name='Дата отправки поста')
    channel = models.ForeignKey(Сhannel, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.description} {self.subscription_level}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('name',)


class Сomments(models.Model):
    user = models.CharField(max_length=70, verbose_name='Nickname пользователя')
    description = models.TextField(verbose_name='Комментарий')
    time_the_comment = models.DateTimeField(verbose_name='Дата отправки комментария')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.user} {self.description}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('user',)
