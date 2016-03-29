from django.test import TestCase

from sentiment140_api import Sentiment140API
from ..twitter_api import *

# Create your tests here.

def main():
	s = Sentiment140API("barry.mingley@gmail.com")
	print bulk_classify_conversations([TweetConversation.objects.all()[0]])
main()
