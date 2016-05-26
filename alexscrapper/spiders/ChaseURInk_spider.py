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



class ChaseURInkSpider(CrawlSpider):
    store_name = "Chase UR (Ink)"
    name = "chaseurink"

    allowed_domains = ["cashbackmonitor.com"]

    start_urls =    ['http://www.cashbackmonitor.com/credit-card-points-comparison/']

    base_url = 'https://www.chase.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }

    searchurls = 'http://www.cashbackmonitor.com/credit-card-points-comparison/{}/'
    path = ['1','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    
    def __init__(self, *args, **kwargs):
        super(ChaseURInkSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')


    def start_requests(self):
        for p in self.path:
            url = self.searchurls.format(p)
            yield Request(url=url, callback=self.parse_product, headers=self.headers)

    def parse_product(self, response):
        item    = Yaging()
        tr      = response.xpath('//table[@class="cbm"]/tr[not(@class="s13")]')
        tr      = tr[:-1]

        for td in tr:
            if len(td.xpath('td[6]/div/a/text()')):
                name        = str(td.xpath('td[1]/a/text()').extract_first().encode('utf-8'))
                link        = str(td.xpath('td[6]/div/a/@href').extract_first())
                cashback    = str(td.xpath('td[6]/div/a/text()').extract_first().encode('utf-8'))
                item['name']        = name.replace("\r\n", "").replace("'", "''")
                item['link']        = self.base_url + link
                item['cashback']    = cashback.replace("'", "''")
                item['sid']         = self.store_name
                item['ctype']       = 1
                item['numbers']     = self.getNumbers(cashback).replace('%', '').replace('$', '')
                item['domainurl']   = self.base_url
                yield item
            elif len(td.xpath('td[6]/a/text()')):
                name        = str(td.xpath('td[1]/a/text()').extract_first().encode('utf-8'))
                link        = str(td.xpath('td[6]/a/@href').extract_first())
                cashback    = str(td.xpath('td[6]/a/text()').extract_first().encode('utf-8'))
                item['name']        = name.replace("\r\n", "").replace("'", "''")
                item['link']        = self.base_url + link
                item['cashback']    = cashback.replace("'", "''")
                item['sid']         = self.store_name
                item['ctype']       = 1
                item['numbers']     = self.getNumbers(cashback).replace('%', '').replace('$', '')
                item['domainurl']   = self.base_url
                yield item
            else:
                pass


    def getNumbers(self, cashback):
        cash = cashback
        pattern = r'\d+(?:\.\d+)?'
        ret =  re.findall(pattern, cash)
        if len(ret):
            return ret[0]
        else:
            return "0"