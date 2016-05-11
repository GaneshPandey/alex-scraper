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



class BanksSpider(CrawlSpider):
    name = "banks"

    allowed_domains = ["cashbackmonitor.com"]

    start_urls =    ['http://www.cashbackmonitor.com/credit-card-points-comparison/']

    base_url = 'http://www.cashbackmonitor.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
        # 'X-App-Id':'44ec0586',
        # 'X-App-Key':'9d6abd7ef1840576f31a022ba48fb92d'

    }

    #path = ['1','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','Y','Z']
    path = ['A']


    def __init__(self, *args, **kwargs):
        super(BanksSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')


    def start_requests(self):
        for p in self.path:
            url = self.start_urls[0]+str(p)
            yield Request(url=url, callback=self.parse_product, headers=self.headers)

    def parse_product(self, response):
        # item = Banks()
        items = Banks()
        pattern = ur'([\d.]+)'
        store = response.xpath('//table[@class="cbm"]/tr[not(@class="s13")]')
        del store[-1]
        item = {}

        for data in store:
            # cashback = data.xpath('td/strong/text()').extract()
            # response.xpath('td[7]').extract()
            items['name'] = data.xpath('td[@class="l tl"]/a/text()').extract()[0]
            items['best'] = self.getBankRate(data.xpath('td[2]').extract())

            # item['link'] =  [self.base_url + link for link in data.xpath('td[@class="l tl"]/a/@href').extract()]
            print "VARIABLE TYPE TOP \n"
            print type(data.xpath('td[2]'))
            print "VARIABLE TYPE TOP\n"
            
            item['Amex_Plenti_Marketplace']    = self.getBankRate(data.xpath('td[2]'))
            item['BarclayCard_Rewardsboost']   = self.getBankRate(data.xpath('td[3]'))
            item['Chase_UR_Freedom']           = self.getBankRate(data.xpath('td[4]'))
            item['Chase_UR_Lnk']               = self.getBankRate(data.xpath('td[5]'))
            item['Chase_UR_Sapphire']          = self.getBankRate(data.xpath('td[6]'))
            item['Wells_Fargo_Rewards']        = self.getBankRate(data.xpath('td[7]'))
                # yield items
            items['bank']    = item
            yield items


    def getBankRate(self, dummy):
        # print "VARIABLE TYPE \n"
        # print len(dummy)
        # print "VARIABLE TYPE \n"
        if dummy[0].xpath('div/a/text()'):
            return dummy[0].xpath('div/a/text()').extract()
        return ""

    def getLink(data):
        return "/techtach"
# response.xpath('//table[@class="cbm"]/tr[not(@class="s13")]')[0].extract()
# title = response.xpath('//table[@class="cbm"]/tr[not(@class="s13")]/td[@class="l tl"]')[0].extract()
# https://api.cartera.com/content/v3/placements?page_id=2395&brand_id=358&section_id=10180&limit=1&offer_tag=info-bar&content_type_id=59