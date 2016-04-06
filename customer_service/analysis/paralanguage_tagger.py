from __future__ import division

from nltk.tokenize import TweetTokenizer

from ..twitter_api.models import *

LOUD_MAX = 2
tokenizer = TweetTokenizer()

def tag_paralanguage(text):
	tokens = tokenizer.tokenize(text)
	#print tokens

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

# Generate contingency table
def generate_contingency_matrix():
	matrix = [[0, 0, 0],
			  [0, 0, 0],
			  [0, 0, 0]]

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

def cell_value(observed, expected):
	return ((observed - expected)**2) / expected

def generate_chi_matrix(table):
	chi_matrix = [[0, 0],
				  [0, 0]]

	total = table[2][2]
	pc =    table[2][0] / total
	no_pc = table[2][1] / total
	pos =   table[0][2] / total
	neg =   table[1][2] / total

	chi_matrix[0][0] = pc * pos * total
	chi_matrix[0][1] = no_pc * pos * total
	chi_matrix[1][0] = pc * neg * total
	chi_matrix[1][1] = no_pc * neg * total

	# For loop!
	chi_matrix[0][0] = cell_value(table[0][0], chi_matrix[0][0])
	chi_matrix[0][1] = cell_value(table[0][1], chi_matrix[0][1])
	chi_matrix[1][0] = cell_value(table[1][0], chi_matrix[1][0])
	chi_matrix[1][1] = cell_value(table[1][1], chi_matrix[1][1])

	return chi_matrix
