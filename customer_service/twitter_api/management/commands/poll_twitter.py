from django.core.management.base import BaseCommand, CommandError

from ...models import *
from ...twitter_util import *

# Constants
screen_names = ['netflixhelps']

class Command(BaseCommand):
    help = 'Pulls Tweets for pre-specificied Twitter accounts'

    def handle(self, *args, **kwargs):
        print "[*] Starting poll_twitter..."
        for screen_name in screen_names:
            print "\t[*] Polling " + screen_name
            find_reply_chains(screen_name)
