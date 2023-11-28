from django.db import models
from main.models import Subscriptions

PAYMENT_METHOD_CHOICES = (
    ('cash', 'Наличные'),
    ('transfer', 'Перевод на счет'),
)


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
