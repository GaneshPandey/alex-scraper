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



class UPromiseSpider(CrawlSpider):
    store_name = "UPromise Online"
    name = "upromise"

    allowed_domains = ["upromise.com"]

    start_urls =    ['https://shop.upromise.com/e/members/benefits.php?sid=132XXdKrlo132&xgroupby=partname&xsearch_type=offer&xletter=z&ajax=z&method=offerJSON&_=1463627668827']

    base_url = 'https://shop.upromise.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }

    path = ['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    searchurls =    'https://shop.upromise.com/e/members/benefits.php?sid=132XXdKrlo132&xgroupby=partname&xsearch_type=offer&xletter={}&ajax={}&method=offerJSON&_=1463627668827'


    def __init__(self, *args, **kwargs):
        super(UPromiseSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')


    def start_requests(self):
        for p in self.path:
            url = self.searchurls.format(p, p)
            yield Request(url=url, callback=self.parse_product, headers=self.headers)

    def parse_product(self, response):
        item = Yaging()
        li = response.xpath("//div/ul/li")
        li = li[1:]
        for l in li:
            name 		= str(l.xpath('a/text()').extract_first())
            cashback 	= str(l.xpath('a/span/text()').extract_first())
            link 		= str(l.xpath('a/@href').extract_first())
            link		= link.replace("\/", "/").replace('\\"', '')
            if "$" in cashback:
                cashback = "$"+ str(self.getNumbers(cashback))
            elif "%" in cashback:
                cashback = str(self.getNumbers(cashback)) + "%"
            else:
                cashback = ""
            item['name']        = name.replace("'", "''")
            item['link']        = self.base_url + link
            item['cashback']    = cashback.replace("'", "''")
            item['sid']         = self.store_name
            item['ctype']       = 1
            item['numbers']     = self.getNumbers(cashback).replace('%', '').replace('$', '')
            item['domainurl']   = self.base_url
            yield item


    def getNumbers(self, cashback):
        cash = cashback
        pattern = r'\d+(?:\.\d+)?'
        ret =  re.findall(pattern, cash)
        if len(ret):
            return ret[0]
        else:
            return "0"