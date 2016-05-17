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



class MrRebatesSpider(CrawlSpider):
    store_name = "Mr Rebates"
    name = "mrrebates"

    allowed_domains = ["mrrebates.com"]

    start_urls =    ['http://www.mrrebates.com/merchants/all_merchants_tabbed.asp']

    base_url = 'http://www.mrrebates.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }

    path = ['#','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


    def __init__(self, *args, **kwargs):
        super(MrRebatesSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')


    def start_requests(self):
        for p in self.path:
            url = self.start_urls[0]+"?letter="+p
            yield Request(url=url, callback=self.parse_product, headers=self.headers)

    def parse_product(self, response):
        item = Yaging()
        pattern = ur'([\d.]+)'
        table = response.xpath('//center/table')
        tr = table.xpath('tr[@class="odd" or @class="even"]')

        for data in tr:
            name        = str(data.xpath('td/a/b/text()').extract()[0])
            link        = str([self.base_url + link for link in data.xpath('td/a/@href').extract()][:][0])
            cashback    = str(data.xpath('td[3]/text()').extract_first().encode('utf-8'))  
            item['name']        = name.replace("'", "''")
            item['link']        = link
            item['cashback']    = cashback.replace("'", "''")
            item['sid']         = self.store_name
            item['ctype']       = 1
            item['numbers']     = self.getNumbers(cashback).replace('$', '').replace('%', '')
            yield item

    def getNumbers(self, cashback):
        cash = cashback
        pattern = r'\d+(?:\.\d+)?%|\$\d+(?:\.\d+)?'
        return re.findall(pattern, cash)[0]

