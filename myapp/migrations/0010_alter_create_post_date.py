# Generated by Django 4.2.17 on 2025-01-06 06:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_create_post_likes_alter_create_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='create_post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 6, 6, 6, 10, 520338)),
        ),
    ]
