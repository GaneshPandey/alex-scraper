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



class IconsumerSpider(CrawlSpider):
    name = "iconsumer"

    allowed_domains = ["iconsumer.com"]

    start_urls =    ['http://www.iconsumer.com/html/storelists.cfm']

    base_url = 'http://www.iconsumer.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }


    def __init__(self, *args, **kwargs):
        super(IconsumerSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')


    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_product, headers=self.headers)

    def parse_product(self, response):
        item = Iconsumer()
        pattern = ur'([\d.]+)'
        store = response.xpath('//div[@class="inner4_blk2"]/ul/li')

        for data in store:
            name = data.xpath('div/a/text()').extract()
            cashback = data.xpath('a[2]/small/text()').extract()
            item['name'] = name
            item['link'] =  [self.parse_link(link) for link in data.xpath('a[2]/@onclick').extract()]
            item['cashback'] = [re.findall(pattern, c) for c in cashback][:][0]
            yield item


    def parse_link(self, jstring):
        start = jstring.find("http")
        end = jstring.find("')")
        return jstring[start:end]