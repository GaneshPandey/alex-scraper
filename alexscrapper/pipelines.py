# aadvantageeshopping
# activejunky
# amtrakGuestRewards
################# banks
# barclaycardrewardsboost
########################### befrugal
# bonuscashcenter
# choiceprivilegesmall
# couponcactus
# discover
# extrabux
# extrarebates
# fatwallet
# #######################################flystore
# givingassistant
# gocashback
######################### hawaiianairlines
# hhonors
# hoopladoopla
# iconsumer
# jetblue
# luckyshops
# mainstreetshares
# mileageplanshopping
# mileageplus
# mrrebates
# plenti
# rebateBlast
# rewards
# rewardsaccelerator
# savingstar
# shopathome
# simplybestcoupons
# skymilesshopping
# southwest
# spirit
# splender
# sunshinerewards
# topcashback
# upromise
# yazing

# -*- coding: utf-8 -*-
import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MySQLStorePipeline(object):
	"""docstring for MySQLStorePipeline"""
	def __init__(self):
		self.conn = MySQLdb.connect("127.0.0.1", "scrapy", "Noones123", "alexspider")
		self.cursor = self.conn.cursor()


	def process_item(self, item, spider):
		try:
			sql = """INSERT INTO `noones` (`s_id`, `name`, `link`, `cashback`, `ctype`, `numb`, `domain`) VALUES ("""+ "'"+item['sid'].encode('utf-8')+ "'," +"'"+item['name'].encode('utf-8')+ "'," +"'"+item['link'].encode('utf-8')+ "'," +"'"+item['cashback'].encode('utf-8') +"'," +"'"+str(item['ctype'])	+"','"+ str(item['numbers']) +"','"+ str(item['domainurl']) + "'" +""")"""
			print sql
			self.cursor.execute(sql)
			self.conn.commit()


		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])

		return item
		self.conn.close()
