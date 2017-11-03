import os
import sys

f = os.path.abspath(os.path.dirname(__file__))
ff = os.path.dirname(f)
fff = os.path.dirname(ff)
sys.path.extend([f, ff, fff])
import codecs
from url_to_intro.info import mysql
from traceback import print_exc


def qu_chong(quchong, log_path):
	with codecs.open(log_path, 'r', 'cp1252') as f:
		for line in f:
			if line not in quchong:
				quchong.add(line)
			else:
				# print('%s, 重复' % line)
				continue


def qingxi(quchong, mysql):
	sql = """insert into weixin_public_guangdong_url (biz, detail_url) VALUES (%s, %s)"""
	cursor = mysql.cursor()
	xxx = []
	for i, line in enumerate(quchong):
		print(i, line)
		try:
			x = line.split('	') if '	' in line else line.split('	')
			if len(x) < 2:
				continue
			biz_b = x[0].replace('??', '')
			url = x[1]
			if not url.startswith('http://mp.weixin.qq.com/s?__biz=') or len(biz_b) != len('3275319549'):
				continue

			xxx.append((biz_b, url))
			if len(xxx) == 1000:
				cursor.executemany(sql, xxx)
				mysql.commit()
				xxx.clear()
			else:
				continue
		except:
			print_exc()
			continue
	cursor.executemany(sql, xxx)
	mysql.commit()


if __name__ == '__main__':
	log_path_list = [
		'/Users/menggui/Desktop/project/weixin/url_to_intro/guandong/电信云测试环境_gzhUrl_广东_1022_{}.log'.format(i) for i in
		range(1, 5)]
	try:
		quchong = set()
		for log_path in log_path_list:
			print(log_path)
			qu_chong(quchong, log_path)
		qingxi(quchong, mysql)
	except:
		print_exc()
	finally:
		mysql.close()
