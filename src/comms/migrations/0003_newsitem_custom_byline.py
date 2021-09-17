# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-09-01 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comms', '0002_auto_20170816_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsitem',
            name='custom_byline',
            field=models.CharField(blank=True, help_text='If you want a custom byline add it here. This will overwrite the display of the user who created the news item with whatever text is added here.', max_length=255, null=True),
        ),
    ]