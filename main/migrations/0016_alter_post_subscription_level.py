# Generated by Django 4.2.7 on 2023-11-14 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_remove_сomments_likes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='subscription_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.subscriptions'),
        ),
    ]
