from nltk.tokenize import TweetTokenizer
from string import maketrans

# Global variables
misc_chars = "$%^&*()-_=+,.<>/?;:'\""
translator = maketrans(misc_chars, "")

tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)

# Removes irrelevant characters such as ':', ',', '"', "'", ';', etc
def remove_misc_chars(text):
	return text.translate(translator)

def remove_hashtags(text):
	pass

def remove_handles(text):
	pass

def remove_urls(text):
	pass

def remove_html_encoding(text):
	pass

def process_text(text):
	#text = remove_misc_chars(text)
	tokens = tokenizer.tokenize(text)

	for i, token in enumerate(tokens):
		# Gets rid of 1 length token that is irrelevant
		if len(token) == 1 and token in misc_chars:
			del tokens[i]	# Should be faster than tokens.remove(token)

		# Gets rid of hashtags
		if token.startswith('#'):
			del tokens[i]
