# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-28 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_post_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='description',
            new_name='inspiration',
        ),
        migrations.RemoveField(
            model_name='post',
            name='hearts',
        ),
        migrations.AlterField(
            model_name='post',
            name='type',
            field=models.SmallIntegerField(),
        ),
    ]
