import json
import requests

"""

"""
class Sentiment140API(object):
	def __init__(self, appid):
		# Constants
		self.BASE_URL = "http://www.sentiment140.com/api/"
		self.BULK_CLASSIFY_JSON_URL = "api/bulkClassifyJson"
		self.NEGATIVE = 0
		self.NEUTRAL  = 2
		self.POSITIVE = 4

		self.raw_appid = appid
		self.appid = "?appid={0}".format(self.raw_appid)

	def __get_request_url(self, action):
		if action == "bulk_classify_conversations":
			return self.BASE_URL + self.BULK_CLASSIFY_JSON_URL + self.appid

	# Classifies a list of Tweets
	def bulk_classify_tweets(self, tweets):
		pass

	"""
		As the largest number of Tweets Sentiment140 allows per request is 5,000, we
		must gather the largest number of conversations whose sum of length of Tweets
		is less than or equal to 5000. In other words, this function groups
		conversations in which each group contains at most 5,000 Tweets between all
		the TweetConversation's in the group.
	"""
	def group_conversations(conversations):
		MAX = 5000
		grouped_conversations = []
		current_group = []
		running_total = 0

		for conversation in conversations.all():
			tweet_count = conversation.tweets.count()

			# If the current conversation's Tweets don't overflow the MAX value, add
			# current conversation to current_gruop array and increase running_total
			if (running_total + tweet_count) < MAX:
				current_group.append(conversation)
				running_total = running_total + tweet_count
			# If the running_total or running_total + tweet_count is larger than MAX,
			# we need to empty the current_group and populate it with the current
			# conversation, starts the process over.
			else:
				running_total = tweet_count
				grouped_conversations.append(current_group)
				current_group = [conversation]

		return grouped_conversations

	"""
		Classifies a list of TweetConversations.

		Algorithm:
			- For each conversation in tweet_conversations.all()
			-	For each tweet in conversation.tweets.all()
			-		Create new dictionary per data format
			-		Append to list
			- Make the Sentiment140 request
			- Create new dictionary to be returned to user
			- For each element in returned_json['data']:
			-	if TweetConversation doesn't exist in new dict:
			-		Add new key with TweetCoversation.id
			-		Add "tweets" key and init it to []
			- Append new dict in Returned data format to "tweets"
	"""
	def classify_conversations(self, tweet_conversations):
		post_dict = {"data" : []}
		return_dict = {}
		request_url = self.__get_request_url("bulk_classify_conversations")

		for conversation in tweet_conversations:
			for tweet in conversation.tweets.all():
				post_dict['data'].append({
					"text" : tweet.text,
					"tweet_id" : tweet.id,
					"tweet_conversation_id" : conversation.id
				})

		response = requests.post(request_url, json=post_dict)
		response = response.json()

		for classified_tweet in response['data']:
			tw_id = classified_tweet['tweet_conversation_id']
			tw = return_dict.get(tw_id, False)

			if not tw:
				return_dict[tw_id] = {
					"tweets" : []
				}

			return_dict[tw_id]["tweets"].append({
				"tweet_id" : classified_tweet['tweet_id'],
				"polarity" : classified_tweet['polarity']
			})

		return return_dict

	"""
		Can take all TweetConversations and classify them all.
	"""
	def bulk_classify_conversations(self, all_conversations):
		conversations = self.group_conversations(all_conversations)

		return [self.classified_conversations(conversation) for conversation in conversations]


"""
	Goals: Be able to classify multiple conversations at once.
	As Sentiment140 supports arbitary fields in JSON requests, we will use this
	feature to identify each TweetConversation and Tweet object.
	Sentiment140 data format:
		Sentiment140 expects an array in a JSON object. Each element of this array
		will look like this:
		{
			"text" : Tweet.text,
			"tweet_conversation_id" : TweetConversation.id,
			"tweet_id" : Tweet.id
		}

	Returned data format:
		[
			"tweet_conversation.id" : {
				"tweets" : [
					{
						"tweet_id" : tweet_id,
						"polarity" : polarity
					},
				]
			}
		]
"""
