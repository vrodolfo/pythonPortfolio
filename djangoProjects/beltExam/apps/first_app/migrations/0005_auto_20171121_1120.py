# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0004_auto_20171121_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trips',
            name='date_from',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='trips',
            name='date_to',
            field=models.DateTimeField(),
        ),
    ]
