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
	# custom_settings = {
	# 	'DOWNLOAD_DELAY': 3,
	# 	'DOWNLOADER_MIDDLEWARES': {
	#
	# 		'get_info.middlewares.RetryMiddleware': 110,
	# 		'get_info.middlewares.RotateUserAgentMiddleware': 2,
	# 	}
	# }

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
			yield scrapy.Request(url_dt, dont_filter=True, meta={'dont_redirect': True, 'item': item, 'retrys': 0})

	def parse(self, response):
		item = response.meta.get('item', {})
		if not item:
			return
		retrys = response.meta.get('retrys', 0)
		if retrys > 4:
			return
		if '验证码' in response.text:
			retrys += 1
			print('check')
			yield scrapy.Request(response.request.url, meta={'item': item, 'retrys': retrys}, dont_filter=True)
		else:
			select = Selector(response=response)
			feature = select.xpath('//ul[@class="profile_desc"]/li[1]/div/@title').extract_first()
			item["feature"] = feature
			# print(item['pub_name'] + "~~~~~~~~" + str(feature))
			yield item
