import json
from urlparse import urlparse

START_URL_CONFIG = []
app_names = ''
APP_NAMES_FILE = 'app_names.txt'

def get_app_name(link):
    url_object = urlparse(link)
    hostname_components = url_object.hostname.split('.')
    if len(hostname_components) == 3:
        return hostname_components[1]
    else:
        return hostname_components[0]

with open('start_url_config.json') as in_file:
    START_URL_CONFIG = json.load(in_file)
    for config in START_URL_CONFIG:
    	link = config['link']
    	app_name = get_app_name(link)
    	app_names = app_names + app_name + '\n'

with open(APP_NAMES_FILE, 'w') as out_file:
	out_file.write(app_names)