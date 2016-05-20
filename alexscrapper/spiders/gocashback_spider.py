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



class GoCashBackSpider(CrawlSpider):
    store_name = "Go CashBack"
    name = "gocashback"

    allowed_domains = ["gocashback.com"]

    start_urls =    ['http://www.gocashback.com/stores']

    base_url = 'http://www.gocashback.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }


    def __init__(self, *args, **kwargs):
        super(GoCashBackSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')

    def start_requests(self):
        for x in xrange(1,6):
            url = "http://www.gocashback.com/stores?p=" + str(x)
            yield Request(url=url, callback=self.parse_product, headers=self.headers)

    def parse_product(self, response):
        item = Yaging()
        stores = response.xpath('//div[@class="top clearfix"]')

        for data in stores:
            name = data.xpath('div[@class="right"]/a/text()').extract()[0].encode('utf-8')
            cashback = data.xpath('div[@class="left"]/p/text()').extract()[0]
            link =  [self.base_url+link for link in data.xpath('div[@class="left"]/a/@href').extract()][0]
            item['name']        = name.replace("'", "''")
            item['link']        = link
            if "$" in cashback:
                cashback = "$"+ str(self.getNumbers(cashback))
            elif "%" in cashback:
                cashback = str(self.getNumbers(cashback)) + "%"
            else:
                pass
            item['cashback']    = self.getCleanName(cashback).replace("'", "''")
            item['sid']         = self.store_name
            item['ctype']       = 1
            item['numbers']     = self.getNumbers(cashback).replace('$', '').replace('%', '')
            item['domainurl']   = self.base_url
            yield item


    def getCleanName(self, s):        
        return s.replace('\\u00a0', ' ')

    def getCleanCashback(self, cashback):
        return cashback


    def getNumbers(self, cashback):
        cash = cashback
        pattern = r'\d+(?:\.\d+)?'
        ret =  re.findall(pattern, cash)
        if len(ret):
            return ret[0]
        else:
            return "100"

