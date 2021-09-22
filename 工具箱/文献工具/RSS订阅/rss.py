import feedparser
import time
import pprint
database = {"cities":"http://rss.sciencedirect.com/publication/science/02642751"}
d = feedparser.parse(database["cities"])


pprint.pprint(d)