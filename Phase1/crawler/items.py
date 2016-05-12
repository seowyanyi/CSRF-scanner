import json
import os

class App:
	def __init__(self, app_name, login, login_link):
		self.app = [{
			"AppName": app_name,
			"Login": login,
			"LoginLink": login_link,
			"AppDetails": []
		}]

	def add_page(self, page):
		self.app[0]["AppDetails"].append(page.get_page())

	def get_app(self):
		return self.app

	def to_string(self):
		return json.dumps(self.app, sort_keys=True, 
			indent=4, separators=(',', ': '))

	def to_file(self, name):
		directory = os.path.dirname(name)
		if not os.path.exists(directory):
		    os.makedirs(directory)
		    print 'created directory {}'.format(directory)

		with open(name, 'w') as outfile:	
			outfile.write(self.to_string())
			print 'Written file {}'.format(name)


class Page:
	def __init__(self, webpage):
		self.webpage = {
			"WebPage": webpage,
			"WebPageLinks": []
		}

	def add_injection_point(self, point):
		self.webpage['WebPageLinks'].append(point.get_point())

	def has_injection_point(self):
		return len(self.webpage['WebPageLinks']) > 0

	def get_page(self):
		return self.webpage 

	def pretty_print(self):
		print json.dumps(self.webpage, sort_keys=True, 
			indent=4, separators=(',', ': '))


class InjectionPoint:
	def __init__(self):
		self.point = {'method': ''}

	def add_method(self, method):
		if method:
			self.point['method'] = method

	def add_param(self, param):
		if param:
			try:
				self.point['params']
			except KeyError:
				self.point['params'] = []
			self.point['params'].append(param)

	def add_action(self, action):
		if action:
			self.point['action'] = action

	def add_href(self, href):
		if href:
			self.point['href'] = href

	def get_point(self):
		return self.point 

	def pretty_print(self):
		print json.dumps(self.point, sort_keys=True, 
			indent=4, separators=(',', ': '))
