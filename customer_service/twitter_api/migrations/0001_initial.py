# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import customer_service.twitter_api.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=customer_service.twitter_api.models.tz_now)),
                ('tweet_created_at', models.DateTimeField()),
                ('tweet_id', models.CharField(max_length=32)),
                ('tweet_text', models.TextField()),
                ('screen_name', models.CharField(max_length=16)),
                ('in_reply_to_status_id', models.CharField(max_length=32, null=True)),
                ('in_reply_to_screen_name', models.CharField(max_length=16, null=True)),
            ],
            options={
                'ordering': ['tweet_created_at'],
            },
        ),
        migrations.CreateModel(
            name='TweetConversation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=customer_service.twitter_api.models.tz_now)),
                ('user_screen_name', models.CharField(max_length=16)),
                ('customer_service_screen_name', models.CharField(max_length=16)),
                ('tweets', models.ManyToManyField(to='twitter_api.Tweet')),
            ],
        ),
    ]
