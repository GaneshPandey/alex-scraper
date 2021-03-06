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


class RewardsSpider(CrawlSpider):
    store_name = "Marriott"
    name = "rewards"
    allowed_domains = ["rewards.com"]
    start_urls =    ['https://marriott.rewards.com/earnpoints/allMerchants']
    base_url = 'https://marriott.rewards.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }

    def __init__(self, *args, **kwargs):
        super(RewardsSpider, self).__init__(*args, **kwargs)
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
        div         = response.xpath('//div[@class="merchant-container-list"]')
        for data in div:
            name        = data.xpath('div[@class="merchant-name"]/div/a/text()').extract()[:][0]
            link        = [self.base_url + link for link in data.xpath('div[@class="merchant-name"]/div/a/@href').extract()][:][0]
            cashback      = data.xpath('div[@class="merchant-cashback"]/div/text()').extract()[0].replace('\n', '').replace('\t', '').replace('\r', '')
            item['name']        = name.replace("'", "''")
            item['link']        = link
            item['cashback']    = cashback.replace("'", "''")
            item['sid']         = self.store_name
            item['ctype']       = 2
            item['numbers']     = self.getNumbers(cashback)
            item['domainurl']   = self.base_url
            yield item

    def getNumbers(self, cashback):
        pattern = r'\d+(?:\.\d+)?'
        return re.findall(pattern, cashback)[0]

    