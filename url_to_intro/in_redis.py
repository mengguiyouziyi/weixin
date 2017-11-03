import os
import sys
import time

f = os.path.abspath(os.path.dirname(__file__))
ff = os.path.dirname(f)
fff = os.path.dirname(ff)
sys.path.extend([f, ff, fff])
from url_to_intro.info import mysql, rc

rc.delete('weixin_guangdong', 'weixin_guangdong_yet')
cursor = mysql.cursor()
sql = """select biz, detail_url from weixin_public_guangdong_url"""
cursor.execute(sql)
results = cursor.fetchall()
for i, r in enumerate(results):
	value = r['biz'] + "~" + r['detail_url']
	rc.lpush('weixin_guangdong', value)
	if i % 10000 == 0:
		time.sleep(3)
	print(i, r['biz'])
