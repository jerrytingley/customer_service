from nltk.tokenize import TweetTokenizer

from ..twitter_api.models import *
from analysis_util import time_difference_min

DAY_LOOKUP = [
	"M",
	"T",
	"W",
	"R",
	"F",
	"S",
	"S",
]
tokenizer = TweetTokenizer()

def average_response_time(conversation):
	tweets = conversation.tweets.all()
	tweet_count = conversation.tweets.count()

	average = 0
	i2 = 0
	for i1 in range(tweets.count() - 1):
		# swap?
		average += time_difference_min(tweets[i1].tweet_created_at, tweets[i1 + 1].tweet_created_at)
		average = average / tweet_count
		i2 = i1
	average += time_difference_min(tweets[i2].created_at, tweets[i2 + 1].tweet_created_at)
	average = average / tweet_count

	return average

def is_direct_mention(conversation):
	first_tweet = conversation.objects.first()

	text = first_tweet.tweet_text
	service_name = "@" + first_tweet.customer_service_screen_name

	if service_name in text:
		return 1
	return 0

def sentiment_scores(conversation):
	tweets = conversation.tweets.all()

	max_score = 0
	min_score = 0
	for tweet in tweets:
		text = tweet.tweet_text
		tokens = tokenizer.tokenize(text)

		for token in tokens:
			sentiment_score = sentiment(text)[0]

			if sentiment_score > max_score:
				max_score = sentiment_score
			elif sentiment_score < min_score:
				min_score = sentiment_score

	return (max_score, min_score)

def get_depth(conversation):
	return conversation.tweets.count()

def get_day(conversation):
	return DAY_LOOKUP[conversation.created_at.weekday()]

# Pulls all features from a conversation.
# Returns string to write to a CSV file.
def pull_features(conversation):
	average_response_time = average_response_time(conversation)
	is_direct_mention = is_direct_mention(conversation)
	sentiment_scores = sentiment_scores(conversation)
	depth = get_depth(conversation)
	day = get_day(conversation)

	return "{0},{1},{2},{3},{4},{5}\n".format(average_response_time, is_direct_mention,
											  sentiment_scores[0], sentiment_scores[1], depth, day)
