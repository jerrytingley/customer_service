from django.core.management.base import BaseCommand, CommandError

from ...paralanguage_tagger import *
from ...regression import *

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		"""
		print "Tagging Tweets..."
		for tweet in Tweet.objects.all():
			value = tag_paralanguage(tweet.tweet_text)
			tweet.paralanguage_classification = value
			tweet.save()
		print "Done"
		"""

		"""
		table = generate_contingency_matrix()
		print table
		print
		print generate_chi_matrix(table)
		"""
		conversations = TweetConversation.objects.all()[0:25]
		for conversation in conversations:
			print pull_features(conversation)
