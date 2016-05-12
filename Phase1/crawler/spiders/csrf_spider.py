# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from crawler.items import InjectionPoint, App, Page

class CSRFSpider(scrapy.Spider):
    name = "csrf"

    def __init__(self, start_url='', allowed_domain='', app_name='',
                    login={}, *args, **kwargs):
        super(CSRFSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = [allowed_domain]
        self.app = App(app_name, login, start_url)
        self.is_logged_in = False
        self.login = login
        self.count = 0
        self.app_name = app_name

    def closed(self, reason):
        print '>>>>>>>>>>>> {} pages crawled for {}'.format(self.count, self.app_name)
        self.app.to_file('Phase1/output/' + self.app_name + '/' + self.app_name + '_' + self.login['privilege'] + '.json')

    def log_in(self, response):
        form_number = 0
        # Choose the login form
        for idx, sel in enumerate(response.xpath("//form")):
            if 'username' in sel.extract() or 'password' in sel.extract():
                form_number = idx

        yield scrapy.FormRequest.from_response(
            response,
            formnumber=form_number,
            formdata={
            'username': self.login['user_id'], 
            'password': self.login['password']},
            callback=self.after_login        
        )

    def remove_starting_slash(self, string):
        if len(string) == 0:
            return string
        if string[0] == '/':
            return string[1:]
        return string

    def is_valid_href(self, href):
        blacklist = [
            'newaccount', 'userguide', 'logout', 'localisation/zone',
            'localisation/geo_zone', 'localisation/country', 'localisation/tax_class',
            'localisation/language', 'localisation/length_class', 'localisation/weight_class',
            'localisation/stock_status', 'localisation/order_status', 'extension/total', 'route=catalog',
            'tool/backup', 'route=sale'
        ]
        for i in range(0, len(blacklist)):
            if blacklist[i] in href:
                return False
        return True

    def extract_data(self, response):
        page = Page(response.url)
        # Parse forms
        for sel in response.xpath("//form"):
            point = InjectionPoint()

            form_content = sel.extract()
            form_type = sel.xpath('@method').extract()
            form_action = sel.xpath('@action').extract()
            
            if form_type:
                point.add_method(form_type[0])
            if form_action:
                point.add_action(form_action[0])

            inputs_content = Selector(text=form_content).xpath('//input').extract()

            for i in inputs_content:
                input_name = Selector(text=i).xpath('//@name').extract()
                input_type = Selector(text=i).xpath('//@type').extract()
                input_value = Selector(text=i).xpath('//@value').extract()     
                
                param = {}                           
                if input_name:
                    param['name'] = input_name[0]
                if input_type:
                    param['type'] = input_type[0]
                if input_value:
                    param['value'] = input_value[0]

                point.add_param(param)

            page.add_injection_point(point)

        # Parse links
        for sel in response.xpath("//a"):            
            href = Selector(text=sel.extract()).xpath('//@href').extract()
            if len(href) == 0:
                continue
            else:
                href = href[0]

            # Remove starting slash
            href = self.remove_starting_slash(href)

            if 'edit' in href or 'del' in href:
                point = InjectionPoint()
                point.add_method('get')
                point.add_href(href)
                page.add_injection_point(point)
            elif self.is_valid_href(href):
                url = response.urljoin(href)                
                yield scrapy.Request(url, callback=self.extract_data)

        if page.has_injection_point():
            self.app.add_page(page)
            self.count += 1  

    def after_login(self, response):
        self.is_logged_in = True

        if "log out" in response.body.lower() or "logout" in response.body.lower():
            print 'log in success'
            return self.extract_data(response)
        else:
            print 'log in fail'
            return self.extract_data(response)

    def parse(self, response):
        if not self.is_logged_in:
            return self.log_in(response)
        else:
            return self.after_login(response)

