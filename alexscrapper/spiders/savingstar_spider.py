
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



class SavingStarSpider(CrawlSpider):
    name = "savingstar"
    store_name = "Saving Star"
    
    allowed_domains = ["savingstar.com", "rewardsaccelerator.com"]

    start_urls =    ['https://api.rewardsaccelerator.com/shop/merchants?index=0&key=fc0a-2dd1403e-3295&limit=2000&type=0']

    base_url = 'https://www.savingstar.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }


    def __init__(self, *args, **kwargs):
        super(SavingStarSpider, self).__init__(*args, **kwargs)
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
        j = json.loads(response.body)
        j = j['data']['records']
        for x in xrange(0,len(j)):
            name        = j[x]['merchantName']
            link        = j[x]['redirectURL'].replace("//", "http://")
            cashback    = j[x]['awardMessage']

            item['name']        = name.replace("'", "''")
            item['link']        = link
            if "$" in cashback:
                cashback = "$"+ str(self.getNumbers(cashback))
            elif "%" in cashback:
                cashback = str(self.getNumbers(cashback)) + "%"
            else:
                cashback = ""
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
