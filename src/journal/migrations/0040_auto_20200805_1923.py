# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-05 19:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0039_journal_disable_front_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='issue',
            field=models.CharField(default='1', max_length=255),
        ),
    ]