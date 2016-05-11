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



class BefrugalSpider(CrawlSpider):
    name = "befrugal"

    allowed_domains = ["befrugal.com"]

    start_urls =    ['http://www.befrugal.com/coupons/stores/']

    base_url = 'https://www.befrugal.com'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }


    def __init__(self, *args, **kwargs):
        super(BefrugalSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_product, headers=self.headers)


    def parse_product(self, response):
        item = Befrugal()
        for sel in response.xpath('//article[@class="store"]'):
            _name = sel.xpath('a/@href').extract()
            _name =  [name.split('/')[-1] for name in _name]
            _cash = sel.xpath('a/strong/text()').extract()
            _cash = [cash.split(' ')[-3] for cash in _cash]
            item['link'] =  [self.base_url+link for link in sel.xpath('a/@href').extract()]
            item['name']  = [name.replace("-"," ") for name in _name]
            item['cashback'] = _cash
            yield item
            
    def post(self, data):
        url = "http://www.befrugal.com/coupons/stores/"
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        payload = 'ctl00%24tsm=ctl00%24cntMainLeftContent%24updatePanel%7Cctl00%24cntMainLeftContent%24lnkLetterC&ctl00_tsm_HiddenField=%3B%3BAjaxControlToolkit%2C%20Version%3D4.1.40412.0%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D28f01b0e84b6d53e%3Aen-US%3Aacfc7575-cdee-46af-964f-5d85d9cdcf92%3A475a4ef5%3A5546a2b%3A497ef277%3Aeffe2a26%3Aa43b07eb%3A751cdd15%3Adfad98a5%3A1d3ed089%3A3cf12cf1%3B&ctl00%24hdr%24bfLoginStatus%24hidObjId=&ctl00%24hdr%24bfLoginStatus%24hidObjType=&ctl00%24hdr%24bfLoginStatus%24hidObjPath=&ctl00%24hdr%24bfLoginStatus%24hidFavoriteObjId=&ctl00%24hdr%24bfLoginStatus%24hidFavoriteObjType=&ctl00%24hdr%24bfLoginStatus%24hidLoginUsername=&ctl00%24cntMainLeftContent%24ddlCategories=Show_All&ctl00%24foot%24txtEmail=&ctl00%24neverMissADealSignup%24hdnRetailerName=&ctl00%24neverMissADealSignup%24componentNeverMissADeal%24emailSignup%24txtRetailerName=&ctl00%24neverMissADealSignup%24componentNeverMissADeal%24emailSignup%24txtEmail=&__EVENTTARGET=ctl00%24cntMainLeftContent%24lnkLetterC&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=5jm4sJGp3uEdZk%2BTx7q1S2Q0zQ8ziday2qVIgp%2FP15yUDl2tWvoL6swnjTdW9dhC16Akd1hYiCb8Q%2FAbdkvQwdfQ4NI%3D&__VIEWSTATEGENERATOR=DF720547&__EVENTVALIDATION=%2Futh60gj92%2BTZZPprb64OI7WJfq17i%2FrE39WH%2BSCzeab3y3YqjV7y31kGmsebwqlT4KdvQVRb89WEw9JzrboxCSliiS%2BJ%2BaJPFwgVTHTNe%2BgA68JTw%2BIrSsVUEMs1ja4M9czKD041%2FAKt9q5l0Dfecv5kDukBdExD4e0zUBTrXCBTtp3JF7hjvPZTq2HWpxgKY5E%2FHpVMz3foZoJfXi%2FXNmKQHncgZpVFbezv6uYSwTBWP6ZKFoT6jaQx2KwyhyZ9unTL%2BkCsJW3eStpVnxvySSZ%2FHRHUx%2Fod0KBO%2BEAkEbLyB8FmIF7qv2l2aOGLgKWqy1DEoLu7Q3UCBd%2FK5rkh9vM%2FSG%2B1eU5MKyp6DDXzSggJOcfBa9Jhd136XsRiF%2BGHjWO%2F2%2FbnrNTJbctrbLlfrY48paqrxRss1%2FcH36kq%2F2QRaTA8LEKvylTesCEr9Gm5dtBOIjPGaRRV4i9HBumQFOZpzAIK3x7vVy8jzoDk5TlIifFK%2B0eu%2BaUzq0evhqaZI0bwCmElpLDWVT3gsa59Xrdn5FOtDKDz7OfSEE7razNe5ZxavO5Dg6sxtj2NT%2B5Awgdc5hOJN%2BYrQGAaXnWUfexHwiCMvNQonh%2FVTwWbyCnLv3hqXCLPWfxamU%2BXO1xO6TBpImjO8uuNpZSiigRboWAqvc5FG6%2FTjk%2BWhokSKeoY%2FVYOu2A5sXwOmsIwqk97HFLeEpEdRuUyHolOXxkJodSSlo33DzXEYf4Ymgc5pADW48zOXiF0eSIZ8v%2BgDEbYz2nGknkpWLeiBiWXpJhO4j%2BlsilrBaq0DQuRCZlQVaTPjI4PxHkjcC4yCdkojS%2FvEGiTVVFtraVwYgzz9YcARwfWJk1C9FnTbUS8K%2BhofmUA4R%2Blud63Cl9u1g9YYnhGnSKeYiCwTk3%2FTT8JWsPJ4wcqTLWW6Dzx7SQlRqGGcmhX4NV7K0o04ss6CwN5qRruO%2FABiMLcgyqOQxwa%2BdD4kEGhOJATVsw8FzKCBUV%2BjcNSrqnfTQ8Y1c79iK8XFdfD0Nnp4tfSJ%2FvJ%2FUiOPg%2FhchZKFfndq1L5LA%2FdpyiTd5XqC%2FuMV1xt4Lr3gsSAPhmy9XzzT5SvrFCp0c9CDV1rRkVTpGTvIZF3sZmApQGeeHIQdNG%2FfHwWndVQFxaU2j%2BWJ1wmb6R5m2WIFi49hi2bm2ZxHuh5b%2FKD2PugiRgIwqfuYuBsQiu7SrLvJvntGkYQ4849w4QXQnrLCCdqMq3%2B98s9INpJ3%2FtGYXb8YWDvOeQKT3wdbrfKtShepK8jJrTaPz%2FaqQs4LIlOZnsnGQAxxxMx%2BM%3D&__ASYNCPOST=true&'
        r = requests.post(url, data=payload, headers=headers)


