#import datetime
import json
import time

from django.core.management.base import BaseCommand, CommandError

from ...models import *
from ...twitter_util import *

# Constants
#screen_names = ['netflixhelps']
log_file_name = 'poll_twitter.log'
json_file_name = 'customer_service/twitter_api/config.json'

config = None
with open(json_file_name, 'r') as f:
	config = json.loads(f.read())

screen_names = config['service_screen_names']
#[config['service_screen_names'][0], config['service_screen_names'][1]]
# Swap array around?

class Command(BaseCommand):
	help = 'Pulls Tweets for pre-specificied Twitter accounts'

	def handle(self, *args, **kwargs):
		with open(log_file_name, 'a') as log:
			now = datetime.now()
			start_str = now.strftime(now.strftime("%m/%W/%Y - %H:%M:%S"))
			log.write("[*] Start: " + start_str + "\n")
			print start_str

			for screen_name in screen_names:
				try:
					print
					print "[*] Polling " + screen_name
					print
					find_reply_chains(screen_name)
				except Exception as e:
					print "[!] Rate Limit exceeded"
					print "[!] Sleeping for 15 minutes"
					wake = now + datetime.timedelta(seconds=60 * 15)
					wake_str = wake.strftime(now.strftime("%m/%W/%Y - %H:%M:%S"))
					print "[*] Will wake at " + wake_str
					time.sleep(60 * 15)
					print "[*] Resuming..."
					print

			now = datetime.now()
			end_str = now.strftime(now.strftime("%m/%W/%Y - %H:%M:%S"))
			log.write("End: " + end_str + "\n")
			print "[*] End: " + end_str
