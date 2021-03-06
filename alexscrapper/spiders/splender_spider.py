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
from lxml import html


class SplenderSpider(CrawlSpider):
    store_name = "Splender"
    name = "splender"
    allowed_domains = ["splender.com", "cartera.com", "api.cartera.com"]
    start_urls =    ['https://www.splender.com/api/content/merchants?fl=name,url_safe_name,rebate,categories,class,logoUrl,offers,min_rebate_value']
    base_url = 'https://www.splender.com/#!/stores/2152/'

    headers = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'en-US,en;q=0.8,hi;q=0.6,ar;q=0.4,ne;q=0.2,es;q=0.2',
        'Connection':'keep-alive',
        'Host': 'www.splender.com',
        'secret_token':'60885065c1a94506c8c75936bf795671',
        'access_token': '32fceb644f3952a711935ffb308a80392d43507c',
        'Cache-Control': 'no-cache'
    }

    def __init__(self, *args, **kwargs):
        super(SplenderSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')


    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_product, headers=self.headers)

    def parse_product(self, response):
        item        = Yaging()
        j           = json.loads(response.body)
        for x in xrange(0,len(j['docs'])):
            name        = j['docs'][x]['name']
            link        = j['docs'][x]['url_safe_name']
            cashback    = j['docs'][x]['rebate']['value']
            item['name']        = name.replace("'", "''")
            item['link']        = self.base_url + link
            item['cashback']    = str(cashback) + " " + j['docs'][x]['rebate']['currency']
            item['sid']         = self.store_name
            item['ctype']       = 1
            item['numbers']     = cashback
            item['domainurl']   = self.base_url
            yield item