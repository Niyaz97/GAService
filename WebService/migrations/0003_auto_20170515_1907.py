# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-15 16:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WebService', '0002_auto_20170413_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.CharField(max_length=16)),
                ('endDate', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=32)),
                ('ru', models.CharField(max_length=48)),
                ('en', models.CharField(max_length=48)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('viewId', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='site',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebService.User'),
        ),
        migrations.AddField(
            model_name='chart',
            name='metric',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebService.Metric'),
        ),
        migrations.AddField(
            model_name='chart',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebService.Site'),
        ),
    ]