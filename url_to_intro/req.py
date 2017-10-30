import os
import sys

f = os.path.abspath(os.path.dirname(__file__))
ff = os.path.dirname(f)
fff = os.path.dirname(ff)
sys.path.extend([f, ff, fff])

# import base64
import codecs
import time
import requests
import random
import pymysql
import traceback
from scrapy import Selector

conn = pymysql.connect(host='172.31.215.38', port=3306, user='spider', password='spider', db='spider',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

USER_AGENT_CHOICES = [
	'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
	'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
	'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
	'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
	'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
	'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
	"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
	"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
	"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
	"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
	"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
	"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
	"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
headers = {
	'upgrade-insecure-requests': "1",
	# 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	'user-agent': random.choice(USER_AGENT_CHOICES),
	'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	'accept-encoding': "gzip, deflate, br",
	'accept-language': "zh-CN,zh;q=0.8",
	'cookie': "RK=mANPtD8eQR; pgv_pvi=7332012032; sd_userid=54101497259025450; sd_cookie_crttime=1497259025450; tvfe_boss_uuid=2df455c17b493681; ptui_loginuin=1054542506; pac_uid=1_775618369; ptcz=373bd6a23bc86488efcf835f7b525ab131e8b91a6a31139a4634e4593b1cbf8c; pt2gguin=o0775618369; pgv_info=ssid=s8239819951; pgv_pvid=9631912360; o_cookie=775618369",
	'cache-control': "no-cache",
	'postman-token': "4a5acd0d-e4ac-ac5d-59c4-0e14d582eecf"
}


with codecs.open('weixin_quchong_all_1.log', 'r', 'cp1252') as f:
	for i, line in enumerate(f):
		# if i >= 39000:
		# if i >= 39000:
		if 117000 >= i > 7800:
		# if i >= 39000:
			continue
		print(i)
		try:
			# biz_b = line[:16]
			# url = line[17:]
			# biz_str = base64.urlsafe_b64decode(biz_b)
			x = line.split('	') if '	' in line else line.split('	')
			if len(x) < 2:
				continue
			biz_str = x[0].replace('??', '')
			url = x[1]
			try:
				response = requests.request("GET", url, headers=headers, timeout=5)
			except:
				continue
			biz = int(biz_str)
			sel = Selector(text=response.text)
			weixin_name = sel.xpath('//strong[@class="profile_nickname"]/text()').extract_first()
			p_tags = sel.xpath('//p[@class="profile_meta"]')
			weixin_hao = ''
			feature = ''
			for p_tag in p_tags:
				word = p_tag.xpath('./label[@class="profile_meta_label"]/text()').extract_first()
				sbody = p_tag.xpath('./span[@class="profile_meta_value"]/text()').extract_first()
				if word:
					if '微信号' in word:
						weixin_hao = sbody
					elif '功能介绍' in word:
						feature = sbody
			# weixin_dict = {'name': name, 'weixin_hao': weixin_hao, 'feature': feature}
			# weixin_li.append(weixin_dict)
			sql = """insert into weixin_public_zhejiang (detail_url, biz, weixin_name, weixin_hao, feature) VALUES (%s, %s, %s, %s, %s)"""
			values = [url, biz, weixin_name, weixin_hao, feature]
			sql1 = """insert into weixin_public_zhejiang (detail_url, biz, weixin_name, weixin_hao) VALUES (%s, %s, %s, %s)"""
			values1 = [url, biz, weixin_name, weixin_hao]
			try:
				cursor.execute(sql, values)
			except:
				traceback.print_exc()
				cursor.execute(sql1, values1)
				continue
			finally:
				conn.commit()
				time.sleep(random.randint(4, 7))
		except:
			traceback.print_exc()
			continue
conn.close()
