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



class TopCashBackSpider(CrawlSpider):
    store_name = "Top Cash Back"
    name = "topcashback"

    allowed_domains = ["topcashback.com"]

    start_urls =    ['http://www.topcashback.com/search/merchants/?letter=C&page=0']

    base_url = 'https://topcashback.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }

    searchurls = 'http://www.topcashback.com/search/merchants/?letter={}'
    path = ['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    # path = ['Z']
    def __init__(self, *args, **kwargs):
        super(TopCashBackSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')


    def start_requests(self):
        for p in self.path:
            url = self.searchurls.format(p)
            yield Request(url=url, callback=self.start_page, headers=self.headers)

    def start_page(self, response):
        page    = response.xpath('//div[@class="gecko-pagination"]/a/text()').extract()
        a = ['1', '1', '1', '1']
        page = a + page
        if len(page)!=0:
            for x in xrange(1,int(page[-4])+1):
                url = response.url + "&page=" + str(x)
                print url +"\n"
                yield Request(url=url, callback=self.parse_product, headers=self.headers)
        else:
            url = response.url
            print url
            yield Request(url=url, callback=self.parse_product, headers=self.headers)



    def parse_product(self, response):
        item = Yaging()
        td_2 = response.xpath('//td[@class="gecko-col-description"]')
        td_3 = response.xpath('//td[@class="gecko-btn-col-plus"]')
        for x in xrange(0,len(td_2)):
            name        = str(td_2[x].xpath('a/span/text()').extract_first().encode('utf-8'))
            link        = str(td_2[x].xpath('a/@href').extract_first().encode('utf-8'))
            cashback    = str(td_3[x].xpath('a/span/text()').extract_first().encode('utf-8'))

            item['name']        = name.replace("\r\n", "").replace("'", "''")
            item['link']        = self.base_url + link
            item['cashback']    = cashback.replace("'", "''")
            item['sid']         = self.store_name
            item['ctype']       = 1
            item['numbers']     = self.getNumbers(cashback).replace('%', '').replace('$', '')
            item['domainurl']   = self.base_url
            yield item


    def getNumbers(self, cashback):
        cash = cashback
        pattern = r'\d+(?:\.\d+)?'
        ret =  re.findall(pattern, cash)
        if len(ret):
            return ret[0]
        else:
            return "0"