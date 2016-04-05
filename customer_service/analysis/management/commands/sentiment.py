from customer_service.twitter_api.models import *
from ...sentiment140_api import *

from django.core.management.base import BaseCommand, CommandError
from pprint import pprint as pp

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		api = Sentiment140API("barry.mingley@gmail.com")
		classifications = api.bulk_classify_conversations(TweetConversation.objects.all())
		for classification in classifications:
			for obj in classification:
				conversation = TweetConversation.objects.get(id=obj['tweet_conversation_id'])
				tweet = conversation.tweets.get(id=obj['tweet_id'])
				tweet.sentiment_classification = obj['polarity']
				tweet.save()
		"""
		groups = api.group_conversations(TweetConversation.objects.all()[0:2000])
		print len(groups)
		classification = api.classify_conversations(groups[0])
		pp(classification)
		"""
