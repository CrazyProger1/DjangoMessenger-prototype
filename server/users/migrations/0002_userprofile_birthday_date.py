# Generated by Django 4.0.5 on 2022-07-01 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='birthday_date',
            field=models.DateField(null=True, verbose_name='birthday date'),
        ),
    ]
