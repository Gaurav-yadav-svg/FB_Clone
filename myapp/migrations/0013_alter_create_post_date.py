# Generated by Django 4.2.17 on 2025-01-09 05:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_alter_create_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='create_post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 9, 5, 27, 7, 415050)),
        ),
    ]
