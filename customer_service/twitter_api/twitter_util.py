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

# Retrieves a single status
def get_status(tweet_id):
	return api.GetStatus(tweet_id).AsDict()

def process_text(status):
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
	tweet_text = process_text(status['text'])
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

# Retrieves count amount of statuses
def get_statuses(screen_name, count=DEFAULT_STATUS_COUNT):
	all_statuses = api.GetUserTimeline(screen_name=screen_name,
							   		   include_rts=False,
							   		   exclude_replies=False,
							   		   count=count)

	return [status for status in all_statuses]

"""
def get_reply_statuses(original_status):
	original_status = original_status.AsDict()
	reply_to_id = originalstatus[REPLY_ID]
	reply_to_name = original_status[REPLY_NAME]

	if not is_reply(original_status):
		return None

	while reply_to_id is not '':
		reply_status = get_status(reply_to_id)
		tweet = status_to_tweet(reply_status)

		reply_to_id = reply_status[REPLY_ID]
"""

# Convert each status to a Tweet and add to database.
def add_statuses_to_db(statuses):
	for status in statuses:
		status_to_tweet(status)

def find_reply_chain(service_status):
	service_status = service_status.AsDict()
	service_screen_name = service_status['user']['screen_name']

	"""
	customer_screen_name = ''
	for mention in service_status['user_mentions']:
		if mention['screen_name'] is not service_screen_name:
			customer_service_screen_name = mention['screen_name']
	"""
	customer_screen_name = service_status['user_mentions'][0]['screen_name'] # Iterate

	# This is t0
	service_status['text'] = process_text(service_status)
	if not is_reply(service_status):
		new_conversation = TweetConversation.objects.create(user_screen_name=customer_screen_name,
											 				customer_service_screen_name=service_screen_name)
		new_conversation.tweets.add(status_to_tweet(service_status))

		return new_conversation
	else:
		if not TweetConversation.objects.filter(user_screen_name=customer_screen_name,
												customer_service_screen_name=service_screen_name).exists():
			search_statuses0, search_statuses1 = get_search(service_screen_name, customer_screen_name)
			print
			print search_statuses0
			print "Search 0:"
			for s0 in search_statuses0:
				p(s0.AsDict())
				print
			print "Seach 1:"
			for s1 in search_statuses1:
				p(s1.AsDict())
				print

			search_set0 = set([status_to_tweet(s0) for s0 in search_statuses0])
			search_set1 = set([status_to_tweet(s1) for s1 in search_statuses1])
			total_tweet = search_set0 | search_set1
			"""

			conversation = TweetConversation.objects.filter(user_screen_name=customer_screen_name,
															customer_service_screen_name=service_screen_name)
			for tweet in total_tweet:
				conversation.tweets.add(tweet)
			"""

def find_reply_chains(service_screen_name):
	for status in get_statuses(service_screen_name, count=5):
		status = status.AsDict()
		if (status['lang'] == 'en') and (not Tweet.objects.filter(tweet_id=status['id']).exists()):
			print " 	Discovering reply chains..."
			tweet_conversation = find_reply_chain(status)
		else:
			print "Else"
			print status['lang'] == 'en'
			print status['lang']
			print not Tweet.objects.filter(tweet_id=status['id']).exists()
			print
