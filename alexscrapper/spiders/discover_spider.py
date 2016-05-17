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
from alexscrapper.module import Render
from lxml import html
import requests



class DiscoverSpider(CrawlSpider):
    name = "discover"
    
    allowed_domains = ["discover.com"]

    start_urls =    ['https://www.discover.com/credit-cards/deals/all-merchants.html']

    base_url = 'https://www.discover.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }


    def __init__(self, *args, **kwargs):
        super(DiscoverSpider, self).__init__(*args, **kwargs)
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
        datas = self.get_html(self.start_urls[0])
        for data in datas.xpath('//div[@class="mn_srchListSection"]/ul/li'):
            name                = data.xpath('a[2]/text()').extract()
            cashback            = data.xpath('span/text()').extract_first()
            item['link']        = [self.base_url+link for link in data.xpath('/a[2]/text()').extract()]
            item['name']        = name
            item['cashback']    = cashback
            item['numbers']     = self.getNumbers(cashback).replace('$', '').replace('%', '')
            yield item

    def get_html(self, url):
            r = Render(url)
            result = r.frame.toHtml()
            formatted_result = str(result.toAscii())
            return html.fromstring(formatted_result)

    def getNumbers(self, cashback):
        cash = cashback
        pattern = r'\d+(?:\.\d+)?'
        ret =  re.findall(pattern, cash)
        if len(ret):
            return ret[0]
        else:
            return "100"


