# Generated by Django 4.0.5 on 2022-07-07 13:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('msgs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='sending_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 7, 13, 46, 53, 367477, tzinfo=utc), verbose_name='sending date and time'),
            preserve_default=False,
        ),
    ]
