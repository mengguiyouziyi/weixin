# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from get_info.items import GetInfoItem
from get_info.utils.get1 import get_key
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class InfoSpider(scrapy.Spider):
	name = 'detail'
	custom_settings = {
		'DOWNLOAD_DELAY': 3,
		"DEFAULT_REQUEST_HEADERS": {
			'upgrade-insecure-requests': "1",
			'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			'referer': "http://weixin.sogou.com/weixin?type=2&query=%E9%98%BF%E9%87%8C&ie=utf8&s_from=input&_sug_=n&_sug_type_=1&w=01015002&oq=&ri=4&sourceid=sugg&sut=0&sst0=1504797523468&lkt=0%2C0%2C0&p=40040108",
			'accept-encoding': "gzip, deflate, br",
			'accept-language': "zh-CN,zh;q=0.8",
			'cache-control': "no-cache",
			'postman-token': "04f4983a-91b5-ebc9-1131-136997df33a2"
		}
	}
	cookie = "RK=mANPtD8eQR; pgv_pvi=7332012032; sd_userid=54101497259025450; sd_cookie_crttime=1497259025450; tvfe_boss_uuid=2df455c17b493681; ptui_loginuin=1054542506; pac_uid=1_775618369; pgv_pvid=9631912360; o_cookie=775618369; ptisp=cnc; ptcz=373bd6a23bc86488efcf835f7b525ab131e8b91a6a31139a4634e4593b1cbf8c; pt2gguin=o0775618369; uin=o0775618369; skey=@fZ9Q2huZl",
	cookie_dict = dict((line.split('=') for line in cookie.strip().split(";")))

	def start_requests(self):
		x = 0
		while True:
			weixin_detail = get_key('weixin_detail')
			if not weixin_detail:
				x += 1
				if x > 10:
					raise CloseSpider()
				time.sleep(120)
				continue
			# weixin_details = ['腾讯科技~http://mp.weixin.qq.com/profile?src=3&timestamp=1504751774&ver=1&signature=RPE1cr62WFqkbDhfA9KUGk3nggerrJoxhdtkU4vZSKqYXaxyL3*FqZQiOQ5ErnCjsRlu4eHclZqrY1fZ4g3o6A==', '阿里装饰~http://mp.weixin.qq.com/profile?src=3&timestamp=1504751774&ver=1&signature=3BujAnQm9OKqdljNIfO3-UU-d2Lc1GHe4-Pl6CqxBlsOvaap5OpV-9gsbmLcYJ*GQi9Sp5F1L1*eIiIwgYx0Gw==', '阿里聚安全~http://mp.weixin.qq.com/profile?src=3&timestamp=1504751774&ver=1&signature=RJG4GxEXAWgYFPTDAf53cmRCJFdrbV5NCraU8cXG3IPOle3rx7NME2oHvgudRsfTo3iOy4VhWxKprzwVmeYtcQ==']
			# for weixin_detail in weixin_details:
			lis = weixin_detail.split('~')
			pub_name = lis[0]
			url_dt = lis[1]
			item = GetInfoItem()
			item['pub_name'] = pub_name
			yield scrapy.Request(url_dt, dont_filter=True, cookies=self.cookie_dict, meta={'dont_redirect': True, 'item': item, 'retrys': 0})

	def parse(self, response):
		item = response.meta.get('item', {})
		if not item:
			return
		retrys = response.meta.get('retrys', 0)
		if retrys > 4:
			return
		if '验证码' in response.text:
			retrys += 1
			print('check~~~~~%s' % response.url)
			yield scrapy.Request(response.request.url, meta={'item': item, 'retrys': retrys}, dont_filter=True)
		else:
			select = Selector(response=response)
			feature = select.xpath('//ul[@class="profile_desc"]/li[1]/div/@title').extract_first()
			item["feature"] = feature
			# print(item['pub_name'] + "~~~~~~~~" + str(feature))
			yield item
