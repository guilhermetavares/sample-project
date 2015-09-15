# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20150915_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(max_length=255, null=True, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='address',
            name='neighborhood',
            field=models.CharField(max_length=255, null=True, verbose_name='neighborhood'),
        ),
    ]
