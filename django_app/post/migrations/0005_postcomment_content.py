# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 15:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_postcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='content',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]