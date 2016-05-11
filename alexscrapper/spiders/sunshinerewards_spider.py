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


class SunshineRewardsSpider(CrawlSpider):
    name = "sunshinerewards"

    allowed_domains = ["sunshinerewards.com", "kyamna.com"]

    start_urls =    ['http://kyamna.com/sunshinerewards.html']

    base_url = 'http://www.sunshinerewards.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }

    # path = ['0-9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','Y','Z']

    def __init__(self, *args, **kwargs):
        super(SunshineRewardsSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')


    def start_requests(self):
        for url in self.start_urls:
            # url = self.start_urls[0] + p + "c/all-categories/alpha"
            # url = self.escape_ajax(url)
            yield Request(url=url, callback=self.parse_product, headers=self.headers)

    def parse_product(self, response):
        item 		= SunshineRewards()
        pattern 	= ur'([\d.]+)'
        tr          = response.xpath('//section[@class="main-content col-lg-9 col-md-9 col-sm-9 col-lg-push-3 col-md-push-3 col-sm-push-3"]/table/tr[3]/td/center/table')

        for data in tr:
            name = data.xpath('tr/td[1]/a/@title').extract()
            link = [link for link in  data.xpath('tr/td[1]/a/@href').extract()]
            cashback = data.xpath('tr/td[2]/text()').extract()
            item['name']    = name
            item['link']    = link
            item['cashback']=  cashback
            yield item
    