
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
    store_name = "Discover"
    
    allowed_domains = ["discover.com"]

    start_urls =    ['https://www.discover.com/credit-cards/deals/json/DFS_Public_Page_Offers.json']

    base_url = 'https://www.discover.com/credit-cards/deals/deals-page.html?id={id}&ICMPGN=DEALSPUB_SEARCH_DEALSTILE_TXT'
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
        jdiscover = unicode(response.body, errors='ignore')
        j = json.loads(jdiscover)
        for x in xrange(1,len(j)):
            name        = j[x]['merchantName']
            link        = self.base_url.format(id=j[x]['id'])
            cashback    = j[x]['headline']
            item['name']        = name.replace("'", "''")
            item['link']        = link
            item['cashback']    = self.getCleanCashBack(cashback).replace("'", "''")
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

    def getCleanCashBack(self, cashback):
        if '$' in cashback:
            return "$"+self.getNumbers(cashback)
        elif '%' in cashback:
            return self.getNumbers(cashback)+"%"
        else:
            return cashback
