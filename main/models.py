from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Сhannel(models.Model):
   name = models.CharField(max_length=80, verbose_name='Название канала', unique=True)
   description = models.TextField(verbose_name='Описание канала', **NULLABLE)
   profile_icon = models.ImageField(upload_to='channel/', verbose_name='Фотография канала')

   def __str__(self):
      return f'{self.name} {self.description}' 
   
   class Meta:
      verbose_name = 'Канал'
      verbose_name_plural = 'Каналы'
      ordering = ('name',)

   
class Subscriptions(models.Model):
   name = models.CharField(max_length=60, verbose_name='Название Подписки')
   description = models.TextField(verbose_name='Описание Подписки')
   profile_icon = models.ImageField(upload_to='subscriptions/', verbose_name='Фотография канала')
   strength_of_subscription = models.IntegerField(verbose_name='Чем выше число, тем сильнее подписка')
   amount_per_month = models.IntegerField(verbose_name='Сумма за месяц')
   channel = models.ForeignKey(Сhannel, on_delete=models.CASCADE, **NULLABLE)
   
   def __str__(self):
      return f'{self.name} {self.description} {self.amount_per_month}' 
   
   class Meta:
      verbose_name = 'Подписка'
      verbose_name_plural = 'Подписки'
      ordering = ('name',)


class Post(models.Model):
   name = models.CharField(max_length=70, verbose_name='Название поста')
   photo_post = models.ImageField(upload_to='post/', verbose_name='фотография к посту')
   description = models.TextField(verbose_name='Описание поста', **NULLABLE)
   subscription_level = models.ForeignKey(Subscriptions , on_delete=models.SET_NULL, null=True)
   likes = models.IntegerField(verbose_name='Кол-во лайков', **NULLABLE)
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
   likes = models.IntegerField(verbose_name='Кол-во лайков', **NULLABLE)
   description = models.TextField(verbose_name='Комментарий')
   time_the_comment = models.DateTimeField(verbose_name='Дата отправки комента')
   post = models.ForeignKey(Post, on_delete=models.CASCADE, **NULLABLE)

   def __str__(self):
      return f'{self.description} {self.likes}' 
   
   class Meta:
      verbose_name = 'Комментарий'
      verbose_name_plural = 'Комментарии'
      ordering = ('user',)