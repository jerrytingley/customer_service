"""
	The methods in this file gather Tweets, Tweet Conversations, and populate
	the database.
"""

import time
import twitter

from datetime import datetime, timedelta
from email.utils import parsedate_tz

from models import Tweet, TweetConversation
from pprint import pprint as p

# Constants
REPLY_ID = 'in_reply_to_status_id'
REPLY_NAME = 'in_reply_to_screen_name'
DEFAULT_STATUS_COUNT = 50

# OAuth information, apps.twitter.com
consumer_key = 'DsxRHf73C6o2HLHIrFQSisrUp'
consumer_secret = 'lN5tvuZpNWAH3TkMWboBEplTmvezNSUp1c445iglizzJVVLeAN'
access_token_key = '4896491896-OM3jLihqIf6xImy62pS2t1xP3M9Z9gZavPQ86kA'
access_token_secret = '57L7TvOtHjADtEpkQsi30612zifAjgr3DsaC3m9RHzogt'

api = twitter.Api(consumer_key=consumer_key,
				  consumer_secret=consumer_secret,
				  access_token_key=access_token_key,
				  access_token_secret=access_token_secret)

def get_search_string(service_screen_name, customer_screen_name, count=DEFAULT_STATUS_COUNT):
	return ("q=from%3A{0}%20to%3A{1}&count={2}".format(service_screen_name, customer_screen_name, count),
			"q=from%3A{0}%20to%3A{1}&count={2}".format(customer_screen_name, service_screen_name, count))

def get_search(service_screen_name, customer_screen_name, count=DEFAULT_STATUS_COUNT):
	search_string0, search_string1 = get_search_string(service_screen_name, customer_screen_name, count)
	searches0 = api.GetSearch(raw_query=search_string0)
	searches1 = api.GetSearch(raw_query=search_string1)

	return ([s0.AsDict() for s0 in searches0],
			[s1.AsDict() for s1 in searches1])

# Converts the Date Time string from the value of status's key 'created_at'.
# http://stackoverflow.com/a/7704266
def created_at_to_datetime(created_at):
    time_tuple = parsedate_tz(created_at.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1])

# Checks if REPLY_ID exists
def is_reply(status):
    if REPLY_ID in status:
        return True
    return False

def status_exists(status):
	return Tweet.objects.filter(tweet_id=status['id']).exists()

# Retrieves a single status
def get_status(tweet_id):
	return api.GetStatus(tweet_id).AsDict()

# Retrieves count amount of statuses
def get_statuses(screen_name, count=DEFAULT_STATUS_COUNT):
	all_statuses = api.GetUserTimeline(screen_name=screen_name,
							   		   include_rts=False,
							   		   exclude_replies=False,
							   		   count=count)

	return [status.AsDict() for status in all_statuses]

def process_text(status):
	status_text = status['text']
	if 'user_mentions' in status:
		for mention in status['user_mentions']:
			screen_name = "@" + mention['screen_name']
			status_text = status_text.replace(screen_name, '')

	if 'hashtags' in status:
		for hash_tag in status['hashtags']:
			hash_tag = "#" + hash_tag
			status_text = status_text.replace(hash_tag, '')

	return status_text

# Converts a Status object returned from get_status to create a a new Tweet.
def status_to_tweet(status):
	tweet_created_at = created_at_to_datetime(status['created_at'])
	tweet_id = status['id']
	tweet_text = process_text(status)
	screen_name = status['user']['screen_name']
	in_reply_to_status_id = status.get(REPLY_ID, None)
	in_reply_to_screen_name = status.get(REPLY_NAME, None)

	tweet = Tweet.objects.create(tweet_created_at=tweet_created_at,
								 tweet_id=tweet_id,
								 tweet_text=tweet_text,
								 screen_name=screen_name,
								 in_reply_to_status_id=in_reply_to_status_id,
								 in_reply_to_screen_name=in_reply_to_screen_name)

	return tweet

def check_status(status):
	exists = status_exists(status)
	in_conversation = TweetConversation.objects.filter(tweets__tweet_id=status['id']).exists()

	return not exists and not in_conversation

# This function only needs to create a new TweetConversation and add Tweets to it!!
# This function takes a status from a customer service account, discovers
# the whole conversation that it's in, creates a new TweetConversation
# and adds it to the database. The beauty of find_reply_chain and find_reply_chains
# is that find_reply_chain only needs one status in the conversation to
# discover the whole conversation which includes the elusive t_n+1 status.
def find_reply_chain(service_status):
	service_screen_name = service_status['user']['screen_name']

	"""
	customer_screen_name = ''
	for mention in service_status['user_mentions']:
		if mention['screen_name'] is not service_screen_name:
			customer_service_screen_name = mention['screen_name']
	"""
	customer_screen_name = service_status['user_mentions'][0]['screen_name'] # Iterate

	# If we discover a part of the conversation that belongs to an existing conversation
	if TweetConversation.objects.filter(user_screen_name=customer_screen_name,
										customer_service_screen_name=service_screen_name).exists():
		conversation = TweetConversation.objects.get(user_screen_name=customer_screen_name,
													 customer_service_screen_name=service_screen_name)

	else:
		conversation = TweetConversation.objects.create(user_screen_name=customer_screen_name,
														customer_service_screen_name=service_screen_name)

	search_statuses0, search_statuses1 = get_search(service_screen_name, customer_screen_name)

	#search_set0 = set([status_to_tweet(s0) for s0 in search_statuses0 if not status_exists(s0)])
	#search_set1 = set([status_to_tweet(s1) for s1 in search_statuses1 if not status_exists(s1)])
	search_set0 = set([status_to_tweet(s0) for s0 in search_statuses0 if check_status(s0)])
	search_set1 = set([status_to_tweet(s1) for s1 in search_statuses1 if check_status(s1)])
	total_tweet = search_set0 | search_set1

	for tweet in total_tweet:
		conversation.tweets.add(tweet)

	return conversation

# We may find additional Tweets in an existing conversation and should check for that
def find_reply_chains(service_screen_name):
	for status in get_statuses(service_screen_name, count=DEFAULT_STATUS_COUNT):
		english = status['lang'] == 'en'
		tweet_exists = Tweet.objects.filter(tweet_id=status['id']).exists() # Make sure this Tweet doesn't already exist. For overlapping searches.
		if english and not tweet_exists:
			print " 	Discovering reply chains..."
			tweet_conversation = find_reply_chain(status)
		else:
			print "Else"
			print english
			print status['lang']
			print tweet_exists
			print
