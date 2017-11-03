import os
import sys

f = os.path.abspath(os.path.dirname(__file__))
ff = os.path.dirname(f)
fff = os.path.dirname(ff)
sys.path.extend([f, ff, fff])

import time
import requests
import random
from traceback import print_exc
from url_to_intro.info import mysql, rc, USER_AGENT_CHOICES
from scrapy import Selector

headers = {
	'upgrade-insecure-requests': "1",
	'user-agent': random.choice(USER_AGENT_CHOICES),
	'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	'accept-encoding': "gzip, deflate, br",
	'accept-language': "zh-CN,zh;q=0.8",
	'cookie': "RK=mANPtD8eQR; pgv_pvi=7332012032; sd_userid=54101497259025450; sd_cookie_crttime=1497259025450; tvfe_boss_uuid=2df455c17b493681; ptui_loginuin=1054542506; pac_uid=1_775618369; ptcz=373bd6a23bc86488efcf835f7b525ab131e8b91a6a31139a4634e4593b1cbf8c; pt2gguin=o0775618369; pgv_info=ssid=s8239819951; pgv_pvid=9631912360; o_cookie=775618369",
	'cache-control': "no-cache",
	'postman-token': "4a5acd0d-e4ac-ac5d-59c4-0e14d582eecf"
}

cursor = mysql.cursor()
while 1:
	line = rc.blpop('weixin_zhejiang')
	if not line:
		print('no url')
		mysql.close()
		sys.exit(1)
	x = line.split('~')
	biz = x[0]
	url = x[1]
	try:
		response = requests.request("GET", url, headers=headers, timeout=5)
	except:
		continue
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
	sql = """insert into weixin_public_zhejiang (detail_url, biz, weixin_name, weixin_hao, feature) VALUES (%s, %s, %s, %s, %s)"""
	values = [url, biz, weixin_name, weixin_hao, feature]

	try:
		cursor.execute(sql, values)
	except:
		print_exc()
		sql1 = """insert into weixin_public_zhejiang (detail_url, biz, weixin_name, weixin_hao) VALUES (%s, %s, %s, %s)"""
		values1 = [url, biz, weixin_name, weixin_hao]
		cursor.execute(sql1, values1)
		continue
	finally:
		print(biz)
		mysql.commit()
		time.sleep(random.randint(3, 6))
