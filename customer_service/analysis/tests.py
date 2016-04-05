#from django.test import TestCase

#from sentiment140_api import Sentiment140API
#from ..twitter_api import *
from paralanguage_tagger import *

# Create your tests here.

def main():
	print tag_paralanguage("BAD")
	print tag_paralanguage("Bad")
	print tag_paralanguage("i dont like netflix!!!!")
main()
