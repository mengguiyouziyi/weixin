import os
import sys

f = os.path.abspath(os.path.dirname(__file__))
ff = os.path.dirname(f)
fff = os.path.dirname(ff)
sys.path.extend([f, ff, fff])
from url_to_intro.info import mysql, rc

rc.delete('weixin_zhejiang', 'weixin_zhejiang_yet')
cursor = mysql.cursor()
sql = """select biz, detail_url from weixin_public_zhejiang_url"""
cursor.execute(sql)
results = cursor.fetchall()
for i, r in enumerate(results):
	value = r['biz'] + "~" + r['detail_url']
	rc.lpush('weixin_zhejiang', value)
	print(i, r['biz'])
