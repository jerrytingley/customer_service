"""
	The methods in this file gather Tweets, Tweet Conversations, and populate
	the database.
"""

import time
import twitter

import pytz

from datetime import datetime, timedelta
from email.utils import parsedate_tz

from models import Tweet, TweetConversation
from pprint import pprint as p

# Constants
REPLY_ID = 'in_reply_to_status_id'
REPLY_NAME = 'in_reply_to_screen_name'
DEFAULT_STATUS_COUNT = 150

# OAuth information, apps.twitter.com
consumer_key = 'mvToNEvVDCLII8ex7oUHEJmv4'
consumer_secret = 'hj6ubN8riXTvHlUFKtn6TProLBQkxcUsZCL2xgiEX866xkNe2v'
access_token_key = '4896491896-OM3jLihqIf6xImy62pS2t1xP3M9Z9gZavPQ86kA'
access_token_secret = '57L7TvOtHjADtEpkQsi30612zifAjgr3DsaC3m9RHzogt'

api = twitter.Api(consumer_key=consumer_key,
				  consumer_secret=consumer_secret,
				  access_token_key=access_token_key,
				  access_token_secret=access_token_secret)
"""
def get_search_string(service_screen_name, customer_screen_name, count=DEFAULT_STATUS_COUNT):
	return ("q=from%3A{0}%20to%3A{1}&count={2}".format(service_screen_name, customer_screen_name, count),
			"q=from%3A{0}%20to%3A{1}&count={2}".format(customer_screen_name, service_screen_name, count))
"""

def get_search_string(service_screen_name, customer_screen_name, count=DEFAULT_STATUS_COUNT):
	search_string = "q=%28from%3A{0}%20%40{1}%29".format(service_screen_name, customer_screen_name)
	search_string += "%20OR%20"
	search_string += "%28from%3A{0}%20%40{1}%29&count={2}".format(customer_screen_name, service_screen_name, count)

	return search_string

def get_search(service_screen_name, customer_screen_name, count=DEFAULT_STATUS_COUNT):
	search_string = get_search_string(service_screen_name, customer_screen_name, count)
	search = api.GetSearch(raw_query=search_string)

	return [s.AsDict() for s in search]

"""
# Converts the Date Time string from the value of status's key 'created_at'.
# http://stackoverflow.com/a/7704266
def created_at_to_datetime(created_at):
    time_tuple = parsedate_tz(created_at.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1])
"""

def created_at_to_datetime(created_at):
	str_format = '%a %b %d %H:%M:%S +0000 %Y'
	date_time = datetime.strptime(created_at, str_format).replace(tzinfo=pytz.UTC)

	return date_time

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

"""
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
"""

# Converts a Status object returned from get_status to create a a new Tweet.
def status_to_tweet(status):
	tweet_created_at = created_at_to_datetime(status['created_at'])
	tweet_id = status['id']
	tweet_text = status['text'] #process_text(status)
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

	customer_screen_name = service_status['in_reply_to_screen_name'] #service_status['user_mentions'][0]['screen_name'] # Iterate

	# If we discover a part of the conversation that belongs to an existing conversation
	if TweetConversation.objects.filter(user_screen_name=customer_screen_name,
										customer_service_screen_name=service_screen_name).exists():
		conversation = TweetConversation.objects.get(user_screen_name=customer_screen_name,
													 customer_service_screen_name=service_screen_name)

	else:
		conversation = TweetConversation.objects.create(user_screen_name=customer_screen_name,
														customer_service_screen_name=service_screen_name)

	search_statuses = get_search(service_screen_name, customer_screen_name)

	for search_status in search_statuses:
		if not status_exists(search_status):
			search_tweet = status_to_tweet(search_status)
			conversation.tweets.add(search_tweet)

	t0 = conversation.tweets.first()
	try:
		if t0.in_reply_to_status_id != None:
			reply_id = t0.in_reply_to_status_id
			try:
				if not conversation.tweets.filter(tweet_id=reply_id).exists():
					print "[!] Discovered seperate status ({0})".format(reply_id)
					outside_reply = get_status(reply_id)
					conversation.tweets.add(status_to_tweet(outside_reply))
			except twitter.TwitterError:
				print "[!] Was not able to retrieve status ({0})".format(reply_id)
	except Exception:
		pass

	return conversation

# We may find additional Tweets in an existing conversation and should check for that
def find_reply_chains(service_screen_name):
	for status in get_statuses(service_screen_name, count=DEFAULT_STATUS_COUNT):
		english = status['lang'] == 'en'
		tweet_exists = status_exists(status)
		account_exists = is_reply(status) and REPLY_NAME in status

		if english and not tweet_exists and account_exists:
			print "[*] Discovering reply chains..."
			tweet_conversation = find_reply_chain(status)
		else:
			if not english:
				print "[!] Skipping, language is: " + status['lang']
			if tweet_exists:
				print "[!] Skipping, status already exists"

# Returns a TweetConversation if a Tweet with tweet_id exists in it's tweets
def get_tweet_conversation_by_tweet(tweet_id):
	try:
		return TweetConversation.objects.filter(tweets__tweet_id=tweet_id)[0]
	except Exception:
		return None
