import os
import sys
from os.path import dirname

father_path = os.path.abspath(dirname(__file__))
sys.path.append(father_path)
from url_to_intro.info import mysql, rc

cursor = mysql.cursor()
sql = """select * from weixin_public_zhejiang_url"""
cursor.execute(sql)
results = cursor.fetchall()
for i, r in enumerate(results):
	value = r['biz'] + "~" + r['detail_url']
	rc.rpush('weixin_zhejiang', value)
	print(i, r['biz'])
