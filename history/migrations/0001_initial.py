# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model', models.CharField(max_length=255, verbose_name='model')),
                ('key', models.CharField(max_length=255, verbose_name='key')),
                ('action', models.CharField(max_length=255, verbose_name='action')),
                ('date', models.DateTimeField(verbose_name='date')),
            ],
            options={
                'verbose_name': 'history log',
                'verbose_name_plural': 'history logs',
            },
        ),
    ]
