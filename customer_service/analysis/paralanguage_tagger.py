from nltk.tokenize import TweetTokenizer

from ..twitter_api.models import *

LOUD_MAX = 2

tokenizer = TweetTokenizer()
def tag_paralanguage(text):
	tokens = tokenizer.tokenize(text)
	print tokens

	# Test for excessive punctuation
	if text.count('!') > LOUD_MAX:
		return 1

	for token in tokens:
		# Make sure the token is not a single letter and
		# that token is only letters
		if len(token) > 1 and token.isalpha():
			# Tests if whole token is upper case
			if token.isupper():
				return 1

			loud_count = 0
			for letter in token[1:]:  # Skip first letter
				if letter.isupper():
					loud_count += 1

			if loud_count > LOUD_MAX:
				return 1

	return 0

def generate_matrix():
	matrix = [[],
			 [],
			 []]

	matrix[0][0] = Tweet.objects.filter(sentiment_classification=4, paralanguage_classification=1).count()
	matrix[0][1] = Tweet.objects.filter(sentiment_classification=4, paralanguage_classification=0).count()
	matrix[0][2] = matrix[0][0] + matrix[0][1]

	matrix[1][0] = Tweet.objects.filter(sentiment_classification=0, paralanguage_classification=1).count()
	matrix[1][1] = Tweet.objects.filter(sentiment_classification=0, paralanguage_classification=0).count()
	matrix[1][2] = matrix[1][0] + matrix[1][1]

	matrix[2][0] = matrix[0][0] + matrix[1][0]
	matrix[2][1] = matrix[0][1] + matrix[1][1]
	matrix[2][2] = matrix[0][2] + matrix[1][2]

	return matrix
