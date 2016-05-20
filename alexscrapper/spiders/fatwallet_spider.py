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



class FatwalletSpider(CrawlSpider):
    store_name = "Fatwallet"
    name = "fatwallet"

    allowed_domains = ["fatwallet.com"]

    start_urls =    ['https://www.fatwallet.com/deals/stores/']

    base_url = 'https://www.fatwallet.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }


    def __init__(self, *args, **kwargs):
        super(FatwalletSpider, self).__init__(*args, **kwargs)
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
        table = response.xpath('//div/table[@class="storeList"]')
        tr1 = table.xpath('tbody/tr[@class="storeListRow"]')
        tr2 = table.xpath('tbody/tr[@class="storeListRow even"]')
        tr = tr1 + tr2

        for data in tr:
            name        = data.xpath('td/a/span/span/text()').extract_first().encode('utf-8')
            cashback    = data.xpath('td[3]/div/span/text()').extract_first()
            link        =  self.base_url+ data.xpath('td/a/@href').extract_first()
            item['name']        = name.replace("'", "''")
            item['link']        = link
            item['cashback']    = cashback.replace("'", "''")
            item['sid']         = self.store_name
            item['ctype']       = 4
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