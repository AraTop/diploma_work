# Generated by Django 4.2.7 on 2023-11-09 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_post_comments_remove_сhannel_post_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptions',
            name='name',
            field=models.CharField(max_length=25, verbose_name='Название Подписки'),
        ),
    ]
