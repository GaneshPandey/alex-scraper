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
			sql = """INSERT INTO `noones` (`s_id`, `name`, `link`, `cashback`, `ctype`) VALUES ("""+ "'"+item['sid'].encode('utf-8')+ "'," +"'"+item['name'].encode('utf-8')+ "'," +"'"+item['link'].encode('utf-8')+ "'," +"'"+item['cashback'].encode('utf-8') +"'," +"'"+str(item['ctype'])	+"'"+""")"""
			print sql
			# sql = """INSERT INTO `noones` (`quote`, `author`, `image`) VALUES ("""+ "'"+item['quote'].encode('utf-8')+ "'," +"'"+item['author'].encode('utf-8')+ "'," +"'"+item['image'].encode('utf-8')+"'"+""")""


			self.cursor.execute(sql)
			self.conn.commit()


		except MySQLdb.Error, e:
			print "Error NNNNN%d: %s" % (e.args[0], e.args[1])

		return item
		self.conn.close()