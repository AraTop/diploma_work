# Generated by Django 4.2.7 on 2023-12-01 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Имя, которое видно всем'),
        ),
    ]