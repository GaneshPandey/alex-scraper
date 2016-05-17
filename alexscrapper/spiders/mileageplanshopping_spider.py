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


class MileagePlanShoppingSpider(CrawlSpider):
    store_name = "Mileage Plan Shopping"
    name = "mileageplanshopping"
    allowed_domains = ["mileageplanshopping.com"]
    start_urls =    ['https://www.mileageplanshopping.com/b____.htm']
    base_url = 'http://mileageplanshopping.com'

    headers = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'en-US,en;q=0.8,hi;q=0.6,ar;q=0.4,ne;q=0.2,es;q=0.2',
        'Connection':'keep-alive',
        'Host':'api.cartera.com',
        'Origin':'https://www.mileageplanshopping.com',
        'Referer':'https://www.mileageplanshopping.com/b____.htm',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36',
        'X-App-Id':'44ec0586',
        'X-App-Key':'9d6abd7ef1840576f31a022ba48fb92d',
        'X-Mem-Id':'Co7ZAuffNM4Hb309Q7nlvw4wY783xZSQdp4iy3ELmQ0rgj2omt9TDb6Zmfh45frFvDsD7/kkCk6wjayefHuFAob8LgabS5+Ctw4NEVaxbmXY+0R5TYzBrFHn1a+dLDaRi2TxkVolMN4QVypp6V8wRlub0o5aIfR2tN0tTn55LdNO5CVBreWl6G/ZZG2mn640sxpQbQ6cFoZhArW8F8y7vPabzgczdD4nmBvq6PNqgGU='
    }

    def __init__(self, *args, **kwargs):
        super(MileagePlanShoppingSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')


    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_product, headers=self.headers)

    def parse_product(self, response):
        print response.body
        item 		= MileagePlanShopping()
        item['name'] = response.body
        yield item
        # pattern 	= ur'([\d.]+)'
        # div         = response.xpath('//div[@class="row thumbnail valign brand appear"]')

        # for data in div:
        #     cashback = data.xpath('div[2]/h5/text()').extract()[:][0]
        #     link = data.xpath('div[1]/h4/a/@href').extract()[:][0]
        #     name = [data.xpath('div[1]/h4/a/text()').extract()][0][0]
        #     item['name']        = name
        #     item['link']        = link
        #     item['cashback']    =  cashback
        #     yield item

        # ctype = 2
    