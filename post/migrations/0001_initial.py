# Generated by Django 4.2.7 on 2023-12-01 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subscription', '0001_initial'),
        ('main', '0024_remove_сomments_post_delete_post_delete_сomments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='Название поста')),
                ('photo_post', models.ImageField(blank=True, null=True, upload_to='post/', verbose_name='фотография к посту')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание поста')),
                ('likes', models.IntegerField(blank=True, default=0, null=True, verbose_name='Кол-во лайков')),
                ('time_the_comment', models.DateTimeField(verbose_name='Дата отправки поста')),
                ('channel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.сhannel')),
                ('subscription_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='subscription.subscriptions')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Сomments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=70, verbose_name='Nickname пользователя')),
                ('description', models.TextField(verbose_name='Комментарий')),
                ('time_the_comment', models.DateTimeField(verbose_name='Дата отправки комментария')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('user',),
            },
        ),
    ]
