from django.db import models

NULLABLE = {'null': True, 'blank': True}

PAYMENT_METHOD_CHOICES = (
   ('cash', 'Наличные'),  
   ('transfer', 'Перевод на счет'),
)


class Сhannel(models.Model):
   name = models.CharField(max_length=20, verbose_name='Название канала', unique=True)
   description = models.TextField(verbose_name='Описание канала', **NULLABLE)
   profile_icon = models.ImageField(upload_to='channel/', verbose_name='Фотография канала', **NULLABLE)

   def __str__(self):
      return f'{self.name} {self.description}' 
   
   class Meta:
      verbose_name = 'Канал'
      verbose_name_plural = 'Каналы'
      ordering = ('name',)

   
class Subscriptions(models.Model):
   name = models.CharField(max_length=15, verbose_name='Название Подписки')
   description = models.CharField(max_length=55, verbose_name='Описание Подписки')
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
   photo_post = models.ImageField(upload_to='post/', verbose_name='фотография к посту', **NULLABLE)
   description = models.TextField(verbose_name='Описание поста', **NULLABLE)
   subscription_level = models.ForeignKey(Subscriptions , on_delete=models.SET_NULL, **NULLABLE)
   likes = models.IntegerField(verbose_name='Кол-во лайков', **NULLABLE , default=0)
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


class Payment(models.Model):
   user_nickname = models.CharField(max_length=10, verbose_name='Пользователь')
   payment_date = models.DateField(verbose_name='Дата оплаты')
   subscriptions = models.ForeignKey(Subscriptions, on_delete=models.CASCADE, verbose_name='Оплаченная подписка')
   amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
   payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')

   def __str__(self):
      return f'{self.user_nickname} - {self.payment_date}'
   
   class Meta:
      verbose_name = 'Платеж'
      verbose_name_plural = 'Платежы'
      ordering = ('user_nickname',)