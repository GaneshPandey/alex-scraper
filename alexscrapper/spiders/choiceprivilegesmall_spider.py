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


class ChoicePrivilegeSmallSpider(CrawlSpider):
    store_name = "Choice Privilege Small"
    name = "choiceprivilegesmall"
    allowed_domains = ["choiceprivilegesmall.com"]
    start_urls =    ['https://www.choiceprivilegesmall.com/az?orderBy=name&page=']
    base_url = 'https://www.choiceprivilegesmall.com/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }

    r = requests.get('https://www.choiceprivilegesmall.com/az?orderBy=name&page=0')
    tree    = html.fromstring(r.text)
    index   = tree.xpath('//div[@class="paging"]/ul/li[7]/a')[0].text
    path    = list(range(int(index)))


    def __init__(self, *args, **kwargs):
        super(ChoicePrivilegeSmallSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')


    def start_requests(self):
        for p in self.path:
            url = self.start_urls[0] + str(p+1)
            yield Request(url=url, callback=self.parse_product, headers=self.headers)

    def parse_product(self, response):
        item 		= Yaging()
        pattern 	= ur'([\d.]+)'
        div         = response.xpath('//div[@class="box-cnt"]/div/div/div[@class="merch-full"]')
        for data in div:
            name        = data.xpath('a/span[2]/text()').extract()[0]
            link        = [self.base_url + link for link in data.xpath('a/@href').extract()][:][0]
            cashback    = data.xpath('a/span[3]/text()').extract_first()
            item['name']        = name.replace("'", "''")
            item['link']        = link
            item['cashback']    = cashback.replace("'", "''")
            item['sid']         = self.store_name
            item['ctype']       = 2
            item['numbers']     = self.getNumbers(cashback).replace('$', '').replace('%', '')
            yield item

    def getNumbers(self, cashback):
        cash = cashback
        pattern = r'\d+(?:\.\d+)?'
        ret =  re.findall(pattern, cash)
        if len(ret):
            return ret[0]
        else:
            return "100"

