# coding:utf-8

import os
import sys
import jieba
import time
from datetime import datetime
from os.path import dirname

import pymysql
from my_redis import QueueRedis

# import io
# import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

father_path = os.path.abspath(dirname(__file__))
sys.path.append(father_path)



def send_key(key):
	mysql = pymysql.connect(host='etl1.innotree.org', port=3308, user='spider', password='spider', db='spider',
	                        charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	try:
		with mysql.cursor() as cursor:
			sql = """select shortname from comp_shortname"""
			sql1 = """select project_nm from project_nm"""
			print('execute begain')
			cursor.execute(sql)
			cursor.execute(sql1)
			results = cursor.fetchall()
			results1 = cursor.fetchall()
			shortnames = [result['shortname'] for result in results]
			project_nms = [result['project_nm'] for result in results1]
			words = []
			short_list = [list(jieba.cut(shortname)) for shortname in shortnames]
			project_list = [list(jieba.cut(project_nm)) for project_nm in project_nms]
			for a in short_list:
				for b in a:
					words.append(b)
			for c in project_list:
				for d in c:
					words.append(d)

			word_set = set(words)

	except Exception as e:
		print(e)
	finally:
		mysql.close()

	red = QueueRedis()

	for word in word_set:
		red.send_to_queue(key, word)
		print(str(word))




if __name__ == '__main__':
	send_key(key='weixin_word')
