# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.spiders import CrawlSpider
from datetime import datetime
from alexscrapper.items import *
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



class HawaiiAnairLinesSpider(CrawlSpider):
    name = "hawaiianairines"

    allowed_domains = ["hawaiianairines.com"]

    start_urls =    ['https://onlinemall.hawaiianairlines.com/emcs/v0.1/comm/data/351']

    base_url = 'https://onlinemall.hawaiianairlines.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'en-US,en;q=0.8,hi;q=0.6,ar;q=0.4,ne;q=0.2,es;q=0.2',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'uuid=8f8365f0ea484d92824ce72fc3a2a828',
        'Host':'nlocate.com',
        'Upgrade-Insecure-Requests':'1'
    }


    def __init__(self, *args, **kwargs):
        super(HawaiiAnairLinesSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36')


    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_product, headers=self.headers)

    def parse_product(self, response):
        item 		= HawaiiAnairLines()
        j           = json.loads(response.body)
        
        for x in xrange(1,len(j['bs'])):
            name        = j['bs'][x]['n']
            domain      = j['bs'][x]['d']
            miles       = str(j['bs'][x]['c']) + " miles per " + str(j['bs'][x]['xs']) + j['bs'][x]['ct']
            item['name']    = name
            item['link']    = domain
            item['miles']   = miles
            yield item