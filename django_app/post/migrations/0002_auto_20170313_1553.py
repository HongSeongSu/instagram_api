# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 06:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterOrderWithRespectTo(
            name='postphoto',
            order_with_respect_to='post',
        ),
    ]
