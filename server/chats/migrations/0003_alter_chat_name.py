# Generated by Django 4.0.5 on 2022-07-06 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_chat_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='chat name'),
        ),
    ]
