# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-15 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebService', '0003_auto_20170515_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='url',
            field=models.CharField(default='', max_length=64),
        ),
    ]