from django.shortcuts import render
from django.views.generic.base import View, TemplateView

from .models import *
from .twitter_util import *

from pprint import pprint as p

class TwitterApiHomeView(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        """
        service_screen_name = 'netflixhelps'
        for status in get_statuses(service_screen_name, 4):
            # Check if status is already in database
            if not Tweet.objects.filter(tweet_id=status['tweet_id']).exists():
                tweet = status_to_tweet(status)

                # Test if this status is a reply
                if is_reply(status):
                    reply_id = status[REPLY_ID]
                    reply_to_tweet = Tweet.objects.get(tweet_id=tweet_id)

                    # Test if there is an existing conversation that contains
                    # the reply Tweet. If so, this status is a part of that
                    # conversations and will be added to it.
                    existing_conversation = TweetConversation.objects.filter(tweets__tweet_id=reply_id)
                    # If existing conversation between two accounts, add new tweet
                    if existing_conversations.exists():
                        existing_conversation.tweets.add(tweet)
                    # Otherwise, create new conversation and add tweet to that
                    else:
                        # Need to check tweet.screen_name != reply_to_tweet.screen_name
                        new_conversation = TweetConversation.objects.create(
                            user_scren_name=reply_to_tweet.screen_name,
                            customer_service_screen_name=service_screen_name)
                        new_conversation.tweets.add(tweet)
        """
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass
