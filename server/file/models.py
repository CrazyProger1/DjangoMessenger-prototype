from django.db import models


class File(models.Model):
    name = models.CharField('File name', max_length=200)
    link = models.CharField('File link', max_length=200)
    message = models.ForeignKey('Message', models.CASCADE)
    encryption_type = models.CharField('Encryption type', max_length=10)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    def __str__(self):
        return f'{self.name}'
