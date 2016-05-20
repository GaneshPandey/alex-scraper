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



class BonusCashCenter(CrawlSpider):
    store_name = "Bonus Cash Center"
    name = "bonuscashcenter"

    allowed_domains = ["bonuscashcenter.com"]

    start_urls =    ['https://www.bonuscashcenter.citicards.com/shopping/b____alpha.htm']

    base_url = 'https://www.bonuscashcenter.citicards.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }


    def __init__(self, *args, **kwargs):
        super(BonusCashCenter, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_product, headers=self.headers)


    def parse_product(self, response):
        li = response.xpath('//div[@class="mn_srchListSection"]/ul/li')
        item = Yaging()
        for l in li:
            name                = l.xpath('a[1]/text()').extract_first()
            cashback            = l.xpath('span/text()').extract_first()
            link                = l.xpath('a[2]/@href').extract_first().replace("../", "/")
            item['link']        = self.base_url+str(link)
            item['name']        = name.replace("'", "''")
            item['cashback']    = cashback.replace("Cash Back", "").replace("'", "''")
            item['ctype']       = 1
            item['sid']         = self.store_name
            item['numbers']     = self.getNumbers(cashback).replace('$', '').replace('%', '')
            item['domainurl']   = self.base_url
            yield item

    def getNumbers(self, cashback):
        cash = cashback
        pattern = r'\d+(?:\.\d+)?%|\$\d+(?:\.\d+)?'
        return re.findall(pattern, cash)[0]