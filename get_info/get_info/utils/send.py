# coding:utf-8

import os
# import jieba
import traceback
from os.path import dirname

import pymysql
from my_redis import QueueRedis

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

father_path = os.path.abspath(dirname(__file__))
sys.path.append(father_path)



def send_key(key):
	mysql = pymysql.connect(host='etl1.innotree.org', port=3308, user='spider', password='spider', db='spider',
	                        charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	try:
		with mysql.cursor() as cursor:
			sql = """select weixin_name from weixin_public"""
			sql1 = """select weixin_name from weixin_public_name_num"""
			print('execute begain')
			words = []

			cursor.execute(sql)
			results = cursor.fetchall()
			shortnames = [result['weixin_name'] for result in results if result]
			# short_list = [list(jieba.cut(shortname)) for shortname in shortnames]
			# for a in short_list:
			# 	for b in a:
			# 		words.append(b)
			for a in shortnames:
				words.append(a)

			print('execute begain 2')
			cursor.execute(sql1)
			results1 = cursor.fetchall()
			project_nms = [result['weixin_name'] for result in results1 if result]
			# project_list = [list(jieba.cut(project_nm)) for project_nm in project_nms]
			# for c in project_list:
			# 	for d in c:
			# 		words.append(d)
			for c in project_nms:
				words.append(c)
			word_set = set(words)

			red = QueueRedis()
			for word in word_set:
				red.send_to_queue(key, word)
				print(str(word))

	except Exception:
		traceback.print_exc()
	finally:
		mysql.close()


if __name__ == '__main__':
	print('你好')
	send_key(key='weixin_word')
