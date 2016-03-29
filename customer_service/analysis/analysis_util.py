import datetime
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup

"""
	Returns HTML of webpage at url.
"""
def get_html(url):
    return urlopen(url).read()

"""
	Loads HTML from webpage at url into a JSON object.
"""
def get_json(url):
	return json.loads(get_html(url))

"""
	Returns a BeautifulSoup object of the HTML of a webpage at url.
"""
def get_remote_soup(url):
    return BeautifulSoup(get_html(url))

"""
	Accepts two datetime instances and returns the difference between them
	in minutes.
"""
def time_difference_min(dt_a, dt_b):
	dt_difference = dt_a - dt_b

	return dt_difference.seconds / 60
