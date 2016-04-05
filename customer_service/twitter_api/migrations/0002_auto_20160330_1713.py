# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweetconversation',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='tweet',
            name='sentiment_classification',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='tweetconversation',
            name='sentiment_classification',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
