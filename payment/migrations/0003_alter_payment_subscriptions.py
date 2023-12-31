# Generated by Django 4.2.7 on 2023-12-01 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
        ('payment', '0002_alter_payment_options_remove_payment_user_nickname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='subscriptions',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription.subscriptions', verbose_name='Оплаченная подписка'),
        ),
    ]
