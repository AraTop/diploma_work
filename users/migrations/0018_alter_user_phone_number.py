# Generated by Django 4.2.7 on 2023-11-19 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.IntegerField(unique=True, verbose_name='Номер телефона без +'),
        ),
    ]
