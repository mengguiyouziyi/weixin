import codecs
import pymysql
from traceback import print_exc

conn = pymysql.connect(host='172.31.215.38', port=3306, user='spider', password='spider', db='spider',
                       charset='utf8', cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
sql = """insert into weixin_public_zhejiang_url (biz, detail_url) VALUES (%s, %s)"""
quchong = set()
try:
	with codecs.open('gzhUrl_zhejiang_1022_quchong.log', 'r', 'cp1252') as f:
		for line in f:
			if line not in quchong:
				quchong.add(line)
			else:
				print('%s, 重复' % line)
				continue
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
				conn.commit()
				xxx.clear()
			else:
				continue
		except:
			print_exc()
			continue
	cursor.executemany(sql, xxx)
	conn.commit()

except:
	print_exc()
finally:
	conn.close()
