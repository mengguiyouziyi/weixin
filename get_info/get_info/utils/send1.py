# coding:utf-8

import os
import sys
from os.path import dirname

import pymysql
from my_redis import QueueRedis

father_path = os.path.abspath(dirname(__file__))
sys.path.append(father_path)


def send_key(key):
	red = QueueRedis()
	mysql = pymysql.connect(host='etl1.innotree.org', port=3308, user='spider', password='spider', db='spider',
	                        charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	cursor = mysql.cursor()
	try:
		loc = 0
		word_set = set()
		while True:
			try:
				cursor.scroll(loc, mode='absolute')
				sql = """select pub_name,url_dt from weixin_base_info where feature='' ORDER by id limit 1000"""
				cursor.execute(sql)
				results = cursor.fetchall()
				pub_names = [result['pub_name'] + '~' + result['url_dt'] for result in results]
				position = len(pub_names)
				for p in pub_names:
					if p in word_set:
						continue
					word_set.add(p)
					red.send_to_queue(key, p)
					print(str(p))
				loc += position
			except Exception as e:
				print(e)
				continue
	except Exception as e:
		print(e)
	finally:
		mysql.close()


if __name__ == '__main__':
	send_key(key='weixin_detail')
