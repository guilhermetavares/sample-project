# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zipcode', models.CharField(max_length=8, verbose_name='zipcode')),
                ('address', models.CharField(max_length=255, verbose_name='address')),
                ('neighborhood', models.CharField(max_length=255, verbose_name='neighborhood')),
                ('state', models.CharField(max_length=2, verbose_name='state')),
                ('city', models.CharField(max_length=255, verbose_name='city')),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
            },
        ),
    ]
