# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-15 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Prediction', '0004_auto_20180315_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predictionresult',
            name='model_number',
            field=models.CharField(max_length=500),
        ),
    ]
