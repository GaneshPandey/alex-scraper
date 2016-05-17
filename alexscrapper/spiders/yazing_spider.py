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


class YangingSpider(CrawlSpider):
    store_name = "Yanging"
    name = "yazing"
    i = 0
    allowed_domains = ["yazing.com"]
    start_urls =    ['http://yazing.com/brands']
    base_url = 'http://yazing.com/deals'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }

    def __init__(self, *args, **kwargs):
        super(YangingSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')


    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_product, headers=self.headers)

    def parse_product(self, response):
        item 		= Yaging()
        pattern 	= ur'([\d.]+)'
        div         = response.xpath('//div[@class="row thumbnail valign brand appear"]')

        for data in div:
            self.i = self.i + 1
            cashback = data.xpath('div[2]/h5/text()').extract()[:][0]
            link = str(data.xpath('div[1]/h4/a/@href').extract()[:][0])
            name = str([data.xpath('div[1]/h4/a/text()').extract()][0][0])
            item['name']        = name.replace("'", "''")
            item['link']        = link
            item['cashback']    = cashback.replace("'", "''")
            item['sid']         = self.store_name
            item['ctype']       = 1
            yield item

    