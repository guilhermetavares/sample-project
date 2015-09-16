# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0003_auto_20150915_0313'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address2',
            field=models.CharField(max_length=255, null=True, verbose_name='address2'),
        ),
    ]
