import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

def tz_now():
	return timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())

def tz_now_date():
	return timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()).date()

class Tweet(models.Model):
	created_at = models.DateTimeField(default=tz_now)
	tweet_created_at = models.DateTimeField()
	tweet_id = models.CharField(max_length=32)
	tweet_text = models.TextField()
	screen_name = models.CharField(max_length=16)
	in_reply_to_status_id = models.CharField(max_length=32, null=True)
	in_reply_to_screen_name = models.CharField(max_length=16, null=True)
	sentiment_classification = models.IntegerField(null=True, blank=True)

	def __unicode__(self):
		return self.tweet_text

	class Meta:
		ordering = ['tweet_created_at']


class TweetConversation(models.Model):
	created_at = models.DateTimeField(default=tz_now)
	user_screen_name = models.CharField(max_length=16)
	customer_service_screen_name = models.CharField(max_length=16)
	sentiment_classification = models.IntegerField(null=True, blank=True)
	tweets = models.ManyToManyField(Tweet)

	def __unicode__(self):
		return "{0} - {1}".format(self.customer_service_screen_name, self.user_screen_name)

	# Mainly used in the shell
	def print_tweets(self, with_screen_name=False):
		for tweet in self.tweets.all():
			if with_screen_name:
				print tweet.screen_name, tweet
			else:
				print tweet

	class Meta:
		ordering = ['-created_at']

# TweetConversation.tweets.all() should return all tweets in proper order
