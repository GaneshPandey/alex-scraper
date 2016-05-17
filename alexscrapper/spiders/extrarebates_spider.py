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
from lxml import html
import requests



class ExtrarebatesSpider(CrawlSpider):
    store_name = "Extra Rebates"
    name = "extrarebates"

    allowed_domains = ["extrarebates.com"]

    start_urls =    ['http://www.extrarebates.com/us/shopping/merchants.php']

    base_url = 'http://www.extrarebates.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }


    def __init__(self, *args, **kwargs):
        super(ExtrarebatesSpider, self).__init__(*args, **kwargs)
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
        table = response.xpath('/html/body/table/tr/td/table[3]/tr/td[2]/table')
        
        td1_name = table.xpath('tr/td[@class=" row1"][2]')
        td2_name = table.xpath('tr/td[@class=" row2"][2]')
        td_name = td1_name + td2_name
        
        td1_cash = table.xpath('tr/td[@class=" row1"][3]')
        td2_cash = table.xpath('tr/td[@class=" row2"][3]')
        td_cash = td1_cash + td2_cash

        td1_link = table.xpath('tr/td[@class=" row1"][4]')
        td2_link = table.xpath('tr/td[@class=" row2"][4]')
        td_link = td1_link + td2_link

        for x in xrange(1,len(td_cash)):
            name            = td_name[x].xpath('span/a/b/text()').extract_first()
            link            = self.base_url + "/" +  td_name[x].xpath('span/a/@href').extract_first()
            cashback        = td_cash[x].xpath('span/b/text()').extract_first()
            if not cashback:
                item['cashback'] = "--"
            else:
                item['cashback']    = cashback.replace("'", "''")

            item['name']        = name.replace("'", "''")
            item['link']        = link
            item['sid']         = self.store_name
            item['ctype']       = 1
            item['numbers']     = self.getNumbers(cashback).replace('$', '').replace('%', '')
            yield item


    def getNumbers(self, cashback):
        return str(cashback)



