import scrapy
from urlparse import urlparse
from scrapy.crawler import CrawlerProcess
from crawler.spiders.csrf_spider import CSRFSpider
import json
import sys

def get_start_url(config):
    return config["link"]

def get_allowed_domain(url):
    return urlparse(url).hostname

def get_app_name(link):
    url_object = urlparse(link)
    hostname_components = url_object.hostname.split('.')
    if len(hostname_components) == 3:
        return hostname_components[1]
    else:
        return hostname_components[0]

def crawl(link, login, process):
	process.crawl(CSRFSpider,
		start_url=link,
		allowed_domain=get_allowed_domain(link),
		app_name=get_app_name(link),
		login=login
	)


START_URL_CONFIG = []
app_name = sys.argv[1]

with open('start_url_config.json') as in_file:
    START_URL_CONFIG = json.load(in_file)

for i in range(0, len(START_URL_CONFIG)):
	config = START_URL_CONFIG[i]
	link = config['link']
	current_app_name = get_app_name(link)
	if current_app_name == app_name:
		process = CrawlerProcess({
			'USER_AGENT': 'Mozilla/4.0 (compatible, MSIE 7.0; Windows NT 5.1)'
		})

		accounts = config['accounts']
		for login in accounts:
			crawl(link, login, process)
		process.start()
		break