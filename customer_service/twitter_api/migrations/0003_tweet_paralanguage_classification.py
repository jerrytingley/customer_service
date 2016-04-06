# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_api', '0002_auto_20160330_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='paralanguage_classification',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
