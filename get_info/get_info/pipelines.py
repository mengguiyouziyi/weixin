# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class MysqlPipeline(object):
	"""
	本机 localhost；公司 etl2.innotree.org；服务器 etl1.innotree.org
	"""

	def __init__(self):
		self.conn = pymysql.connect(host='etl1.innotree.org', port=3308, user='spider', password='spider', db='spider',
		                            charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		if spider.name == 'search':
			# sql = """insert into kuchuan_all(id, app_package, down, trend) VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE app_package=VALUES(app_package), down=VALUES(down), down=VALUES(trend)"""
			sql = """replace into weixin_base_info(pub_name, pic_url, weixin, feature, comp, url_dt)
	                VALUES(%s, %s, %s, %s, %s, %s)"""
			args = (item["pub_name"], item['pic_url'], item["weixin"], item["feature"], item["comp"], item['url_dt'])
			self.cursor.execute(sql, args=args)
			self.conn.commit()
			print(str(item['pub_name']))
		elif spider.name == 'detail':
			sql = """update weixin_base_info set feature=%s WHERE pub_name=%s"""
			args = (item["feature"], item["pub_name"])
			self.cursor.execute(sql, args=args)
			self.conn.commit()
			print(str(item['pub_name']))
