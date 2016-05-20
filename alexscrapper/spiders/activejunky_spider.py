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


class ActivejunkySpider(CrawlSpider):
    store_name = "ActiveJunky"
    name = "activejunky"

    allowed_domains = ["activejunky.com"]

    start_urls = 	['http://activejunky.com/stores?utf8=%E2%9C%93&search_terms=&activity_filters=&min_cashback=&order_by=cashback%3Adesc&page=12&commit=See+More',
					'http://activejunky.com/stores?utf8=%E2%9C%93&search_terms=&activity_filters=&min_cashback=&order_by=cashback%3Adesc&page=11&commit=See+More',
					'http://activejunky.com/stores?utf8=%E2%9C%93&search_terms=&activity_filters=&min_cashback=&order_by=cashback%3Adesc&page=10&commit=See+More',
					'http://activejunky.com/stores?utf8=%E2%9C%93&search_terms=&activity_filters=&min_cashback=&order_by=cashback%3Adesc&page=9&commit=See+More',
					'http://activejunky.com/stores?utf8=%E2%9C%93&search_terms=&activity_filters=&min_cashback=&order_by=cashback%3Adesc&page=8&commit=See+More',
					'http://activejunky.com/stores?utf8=%E2%9C%93&search_terms=&activity_filters=&min_cashback=&order_by=cashback%3Adesc&page=7&commit=See+More',
					'http://activejunky.com/stores?utf8=%E2%9C%93&search_terms=&activity_filters=&min_cashback=&order_by=cashback%3Adesc&page=6&commit=See+More',
					'http://activejunky.com/stores?utf8=%E2%9C%93&search_terms=&activity_filters=&min_cashback=&order_by=cashback%3Adesc&page=5&commit=See+More',
					'http://activejunky.com/stores?utf8=%E2%9C%93&search_terms=&activity_filters=&min_cashback=&order_by=cashback%3Adesc&page=4&commit=See+More',
					'http://activejunky.com/stores?utf8=%E2%9C%93&search_terms=&activity_filters=&min_cashback=&order_by=cashback%3Adesc&page=3&commit=See+More',
					'http://activejunky.com/stores?utf8=%E2%9C%93&search_terms=&activity_filters=&min_cashback=&order_by=cashback%3Adesc&page=2&commit=See+More',
					'http://activejunky.com/stores?utf8=%E2%9C%93&search_terms=&activity_filters=&min_cashback=&order_by=cashback%3Adesc&page=1&commit=See+More'
					]

    base_url = 'https://www.activejunky.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }


    def __init__(self, *args, **kwargs):
        super(ActivejunkySpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_product, headers=self.headers)


    def parse_product(self, response):
        item = Yaging()
        for sel in response.xpath('//article[@class="store"]'):
            _name = sel.xpath('a/@href').extract()
            _name =  [name.split('/')[-1] for name in _name]
            _cash = sel.xpath('a/strong/text()').extract()
            _cash = [cash.split(' ')[-3] for cash in _cash]
            link =  [self.base_url+link for link in sel.xpath('a/@href').extract()][0]
            name  = [name.replace("-"," ") for name in _name][0]
            cashback = _cash[0]
            item['name']        = name.replace("'", "''")
            item['link']        = link
            item['cashback']    = cashback.replace("'", "''")
            item['sid']         = self.store_name
            item['ctype']       = 1
            item['numbers']     = self.getNumbers(cashback).replace('$', '').replace('%', '')
            item['domainurl']   = self.base_url
            yield item
    
    def getNumbers(self, cashback):
        cash = cashback
        pattern = r'\d+(?:\.\d+)?'
        ret =  re.findall(pattern, cash)
        if len(ret):
            return ret[0]
        else:
            return "100"