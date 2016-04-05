import sys

from regression import *

from ..twitter_api.models import *

(average_response_time, is_direct_mention,
sentiment_scores[0], sentiment_scores[1], depth, day)

def main(filename):
	header = "average_response_time,is_direct_mention,max_sentiment,min_sentiment,depth,day\n"

	with open(filename, "wb") as csv_out:
		csv_out.write(header)
		for conversation in TweetConversation.objects.all():
			csv_out.write(pull_features(conversation))

if len(sys.argv) < 1:
	print "filename.csv"
	return -1

print "Generating CSV file..."
main(sys.argv[1])
print "Done"
