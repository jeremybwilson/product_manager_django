# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-20 17:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='udpated_at',
            new_name='updated_at',
        ),
    ]
