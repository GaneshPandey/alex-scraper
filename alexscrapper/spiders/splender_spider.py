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


class SplenderSpider(CrawlSpider):
    name = "splender"

    allowed_domains = ["splender.com"]

    start_urls =    ['https://www.splender.com/#!/stores/']

    base_url = 'http://www.splender.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }

    path = ['0-9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','Y','Z']

    def __init__(self, *args, **kwargs):
        super(SplenderSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')


    def start_requests(self):
        for p in self.path:
            url = self.start_urls[0] + p + "c/all-categories/alpha"
            # url = self.escape_ajax(url)
            yield Request(url=url, callback=self.parse_product, headers=self.headers)

    def parse_product(self, response):
        item 		= SplenderSpider()
        pattern 	= ur'([\d.]+)'
        divs        = response.xpath('//div[@data-ng-repeat="alphaChunk in alphaIndex[letter]"]/div')

        for data in divs:
            item['name']        = data.xpath('merchant-page-link/a/div[1]/text()').extract()
            item['link']        = [self.base_url + link for link in data.xpath('merchant-page-link/a/@ng-href').extract()]
            item['cashback']    = data.xpath('merchant-page-link/a/div[2]/text()').extract()
            yield item
    # ctype = 1