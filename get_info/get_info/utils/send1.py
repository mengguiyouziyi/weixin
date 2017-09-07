# coding:utf-8

import os
import traceback
import time

from os.path import dirname

import pymysql
from my_redis_set import QueueRedis

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

father_path = os.path.abspath(dirname(__file__))
sys.path.append(father_path)


def send_key(key):
	red = QueueRedis()
	mysql = pymysql.connect(host='etl1.innotree.org', port=3308, user='spider', password='spider', db='spider',
	                        charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	cursor = mysql.cursor()
	try:
		loc = 0
		while True:
			# try:
			sql = """select pub_name,url_dt from weixin_base_info where feature='' ORDER by id limit %s, 2000"""
			cursor.execute(sql, (loc,))
			results = cursor.fetchall()
			pub_names = [result['pub_name'] + '~' + result['url_dt'] for result in results]
			for p in pub_names:
				red.send_to_queue(key, p)
				print(1)
			loc += len(pub_names)
			print('等待120秒')
			time.sleep(120)

			# except:
			# 	traceback.print_exc()
			# 	continue
	except:
		traceback.print_exc()
	finally:
		mysql.close()


if __name__ == '__main__':
	send_key(key='weixin_detail')
