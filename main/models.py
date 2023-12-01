from django.db import models

NULLABLE = {'null': True, 'blank': True}


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
