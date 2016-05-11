# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.spiders import CrawlSpider
from alexscrapper.items import *
from datetime import datetime

from scrapy.conf import settings
import urllib
import csv
import json
import re
from datetime import datetime, timedelta
from dateutil import parser
from urllib import urlencode
from HTMLParser import HTMLParser
import requests



class MainStreetSharesSpider(CrawlSpider):
    name = "mainstreetshares"

    allowed_domains = ["mainstreetshares.com"]

    start_urls =    ['https://mainstreetshares.com/retailers.do']

    base_url = 'https://mainstreetshares.com/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }

    path = ['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


    def __init__(self, *args, **kwargs):
        super(MainStreetSharesSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')


    def start_requests(self):
        for p in self.path:
            url = self.start_urls[0]+"?startsWith="+p
            yield Request(url=url, callback=self.parse_product, headers=self.headers)

    def parse_product(self, response):
        item = Yaging()
        pattern = ur'([\d.]+)'
        store = response.xpath('//table/tbody/tr')

        for data in store:
            name = str(data.xpath('td[2]/a/text()').extract()[0])
            cashback = str(data.xpath('td/strong/text()').extract()[0])
            link = str([self.base_url + link for link in data.xpath('td[2]/a/@href').extract()][0])
            item['name']        = name.replace("'", "''")
            item['link']        = link
            item['cashback']    = cashback.replace("'", "''")
            item['sid']         = self.name
            item['ctype']       = 1
            yield item
