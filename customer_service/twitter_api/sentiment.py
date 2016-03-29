from nltk.tokenize import TweetTokenizer

# import sentiwordnet
from .models import Tweet, TweetConversation

# All Tweets authored by a customer service account end with the initials of
# the author, usually in the form "^AB", sometimes omitting the "^". This
# function will extract those initials.
def extract_initials(tweet_text):
	initials = tweet_text[-3:]

	return initials

# This class processes a Tweet and applies a few rules to transform the text.
#class Preprocessor(object):
class Processor(object):
    def __init__(self):
        self.tweet_tokenizer = TweetTokenizer()

    def process(self, tweet):
        text = tweet.tweet_text
        tokens = self.tweet_tokenizer.tokenize(text)

        minimum_index = 0
        maximum_index = len(tokens)
        positivity_total = 0
        negativity_total = 0
        total_tokens = maximum_index
        #for token in tokens:
        for i in range(len(tokens)):
            token = tokens[i]
            if not token.startswith('@') and not token.startswith('#'):


        return text

def classify_tweet(tweet):
    pass
