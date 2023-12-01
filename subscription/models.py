from django.db import models
from subscription.validators import min_sum, validate_non_negative

NULLABLE = {'null': True, 'blank': True}


class Subscriptions(models.Model):
    name = models.CharField(max_length=15, verbose_name='Название Подписки')
    description = models.CharField(max_length=55, verbose_name='Описание Подписки')
    strength_of_subscription = models.IntegerField(verbose_name='Чем выше число, тем сильнее подписка', validators=[validate_non_negative])
    amount_per_month = models.IntegerField(verbose_name='Сумма за месяц', validators=[min_sum])
    channel = models.ForeignKey('main.Сhannel', on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.description} {self.amount_per_month}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('name',)
