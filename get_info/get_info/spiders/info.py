# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from urllib.parse import urljoin
from get_info.items import GetInfoItem
# from get_info.utils.get import get_key
from get_info.settings import SQL_DATETIME_FORMAT


class InfoSpider(scrapy.Spider):
	name = 'info'
	url = 'http://weixin.sogou.com/weixin?query={}&_sug_type_=&sut=1978&lkt=1%2C1504603223573%2C1504603223573&s_from=input&_sug_=y&type=1&sst0=1504603223676&page=1&ie=utf8&w=01019900&dr=1'

	def start_requests(self):
		# while True:
		# 	wx_search = get_key('wx_search')
		wx_search = '阿里'
		if not wx_search:
			raise CloseSpider()
		url = self.url.format(wx_search)
		yield scrapy.Request(url, dont_filter=True, meta={'dont_redirect': True})

	def parse(self, response):
		# print(response.request.meta.get('depth', ''))
		if '相关的官方认证订阅号' in response.text:
			return
		select = Selector(response=response)
		objs = select.xpath('//li[contains(@id, "sogou_vr_11002301_box")]')
		for obj in objs:
			item = GetInfoItem()
			name = obj.xpath('.//div[@class="txt-box"]//p[@class="tit"]/a//text()').extract()
			name = ''.join(name) if name else ''
			# print(name)
			if not name:
				continue

			pic_url = obj.xpath('.//div[@class="img-box"]//img/@src').extract_first()
			weixin = obj.xpath('.//div[@class="txt-box"]//label[@name="em_weixinhao"]//text()').extract_first()
			feature = obj.xpath('./dl[1]/dd//text()').extract()
			feature = ''.join(feature) if feature else ''
			comp = obj.xpath('./dl[2]/dd//text()').extract_first()
			comp = comp if comp else ''

			item["pub_name"] = name
			item["pic_url"] = pic_url
			item["weixin"] = weixin
			item["comp"] = comp
			item["crawlTime"] = datetime.now().strftime(SQL_DATETIME_FORMAT)
			# print(len(feature))
			if len(feature) >= 102:
				url_dt = obj.xpath('.//div[@class="txt-box"]//p[@class="tit"]/a/@href').extract_first()
				# print(name+"~~~~~~~~"+url_dt)
				yield scrapy.Request(url_dt, meta={'item': item, 'retrys': 0}, callback=self.parse_detail, dont_filter=True)
			else:
				item["feature"] = feature
				yield item

		next_url = select.xpath('//a[@id="sogou_next"]/@href').extract_first()
		if next_url:
			next_url = urljoin(response.url, next_url)
			yield scrapy.Request(next_url, dont_filter=True, meta={'dont_redirect': True})

	def parse_detail(self, response):
		item = response.meta.get('item', {})
		retrys = response.meta.get('retrys', 0)
		if retrys > 3:
			return

		if not item:
			return
		if '验证码' in response.text:
			retrys += 1
			# print('验证码：：：status:%s~~~retring~~~title:%s' % (str(response.status), response.url))
			yield scrapy.Request(response.request.url, meta={'item': item, 'retrys': retrys}, callback=self.parse_detail,
			                     dont_filter=True)
		else:
			select = Selector(response=response)
			feature = select.xpath('//ul[@class="profile_desc"]/li[1]/div/@title').extract_first()
			item["feature"] = feature

			# print(item['pub_name'] + "~~~~~~~~" + str(feature))
			yield item
