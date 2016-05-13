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


class HhonorsSpider(CrawlSpider):
    name = "hhonors"

    allowed_domains = ["hhonors.com"]

    start_urls =    ['http://shoptoearn.hhonors.com/loyrewards/earnmall/us/allMerchants']

    base_url = 'http://shoptoearn.hhonors.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }


    def __init__(self, *args, **kwargs):
        super(HhonorsSpider, self).__init__(*args, **kwargs)
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
        tr 			= response.xpath('//div[@class="all-merchant-list"]/div[@class="content-item"]/table/tr')
        for data in tr:
            name        = data.xpath('td[@class="info"]/div/span/a/text()').extract()[:][0].encode('utf-8')
            link        = str(data.xpath('td[@class="merchant-icon"]/table/tr/td/a/@href').extract()[:][0])
            cashback    = str([ self.url_clean(m) for m in data.xpath('td[@class="point-info"]/div[@class="new-point"]/text()').extract()][:][0])
            item['name']        = name.replace("'", "''")
            item['link']        = link
            item['cashback']    = cashback.replace("'", "''")
            item['sid']         = self.name
            item['ctype']       = 2
            yield item

    def url_clean(self, data):
    	data = data.replace(u'\r', '')
    	data = data.replace(u'\t', '')
    	data = data.replace(u'\n', '')
    	data = data.replace(u'  ', '')
    	return data 