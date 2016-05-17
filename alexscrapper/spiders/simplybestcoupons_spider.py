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



class SimplyBestCouponsSpider(CrawlSpider):
    store_name = "Simply Best Coupons"
    name = "simplybestcoupons"

    allowed_domains = ["simplybestcoupons.com"]

    start_urls =    ['https://www.simplybestcoupons.com/Stores']

    base_url = 'https://www.simplybestcoupons.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }

    def __init__(self, *args, **kwargs):
        super(SimplyBestCouponsSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')


    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_product, headers=self.headers)

    def parse_product(self, response):
        item 		= SimplyBestCoupons()
        pattern 	= ur'([\d.]+)'
        li			= response.xpath('//div[@class="StoreList"]/ul/li')
        for data in li:
            item['name']        =  data.xpath('a/text()').extract()
            item['link']        =  [self.base_url + link for link in data.xpath('a/@href').extract()]
            item['cashback']    =  data.xpath('span/text()').extract()
            yield item

# ctype =1