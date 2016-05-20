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



class ExtraBuxSpider(CrawlSpider):
    store_name = "Extra Bux"
    name = "extrabux"

    allowed_domains = ["extrabux.com"]

    start_urls =    ['https://www.extrabux.com/stores/all/']

    base_url = 'https://www.extrabux.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }

    tnum = ""


    def __init__(self, *args, **kwargs):
        super(ExtraBuxSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')
        
    def start_requests(self):
        for x in xrange(1,71):
            url = "https://www.extrabux.com/stores/all/?page=" + str(x)
            yield Request(url=url, callback=self.parse_product, headers=self.headers)

    def parse_product(self, response):
        item = Yaging()
        stores = response.xpath('//div[@class="store"]')

        for data in stores:
            name = data.xpath('div[@class="linkContainer"]/div[@class="oldCashBack"]/a/text()').extract()
            clean_name = []
            for st in name:
                pos = st.find("(")
                clean_name.append(st[0:pos-1].lstrip())

            cashback = data.xpath('div[@class="linkContainer"]/a[@class="cashBack transferLink"]/text()').extract_first()
            item['link'] =  [self.base_url+link for link in data.xpath('a/@href').extract()][0]
            item['name']  = clean_name[0].replace("'", "''")
            if "$" in cashback:
                cashback = "$"+ str(self.getNumbers(cashback))
            elif "%" in cashback:
                cashback = str(self.getNumbers(cashback)) + "%"
            else:
                pass
            item['cashback']    = cashback
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