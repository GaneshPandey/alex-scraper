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


class PlentiSpider(CrawlSpider):
    store_name = "Plenti Online"
    name = "plenti"
    allowed_domains = ["plenti.com", "cartera.com", "api.cartera.com"]
    start_urls =    ['https://api.cartera.com/content/v3/placements?page_id=2395&brand_id=362&section_id=10218&with_offers=1&sort_by=random&content_type_id=58']
    base_url = 'http://plenti.com'

    headers = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'en-US,en;q=0.8,hi;q=0.6,ar;q=0.4,ne;q=0.2,es;q=0.2',
        'Connection':'keep-alive',
        'Host': 'api.cartera.com',
        'X-App-Id': '03617a71',
        'X-App-Key': 'e9d069e72bc241425b5f3d4b1dc8c5bf',
        'Cache-Control': 'no-cache'
    }

    def __init__(self, *args, **kwargs):
        super(PlentiSpider, self).__init__(*args, **kwargs)
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
        for x in xrange(0,len(j['response'])):
            name        = j['response'][x]['merchant']['name']
            link        = j['response'][x]['clickUrl']
            cashback    = j['response'][x]['merchant']['rebate']['value']
            item['name']        = name.replace("'", "''")
            item['link']        = link
            item['cashback']    = str(cashback) + " " + j['response'][x]['merchant']['rebate']['currency']
            item['sid']         = self.store_name
            item['ctype']       = 2
            item['numbers']     = cashback
            item['domainurl']   = self.base_url
            yield item