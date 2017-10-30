# -*- coding: utf-8 -*-
import scrapy
import time
from datetime import datetime
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from urllib.parse import urljoin
from get_info.items import GetInfoItem
from get_info.utils.get import get_key
# from get_info.settings import SQL_DATETIME_FORMAT


class InfoSpider(scrapy.Spider):
	name = 'search'
	url = 'http://weixin.sogou.com/weixin?query={}&_sug_type_=&sut=1978&lkt=1%2C1504603223573%2C1504603223573&s_from=input&_sug_=y&type=1&sst0=1504603223676&page=1&ie=utf8&w=01019900&dr=1'

	def start_requests(self):
		x = 0
		while True:
			wx_search = get_key('weixin_word')
		# for wx_search in ['阿里', '腾讯', '百度']:
			if not wx_search:
				x += 1
				if x > 5:
					raise CloseSpider()
				time.sleep(120)
				continue
			url = self.url.format(wx_search.strip())
			yield scrapy.Request(url, dont_filter=True)

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
			url_dt = obj.xpath('.//div[@class="txt-box"]//p[@class="tit"]/a/@href').extract_first()

			item["pub_name"] = name
			item["pic_url"] = pic_url
			item["weixin"] = weixin
			item["comp"] = comp
			item["url_dt"] = url_dt
			# item["crawlTime"] = datetime.now().strftime(SQL_DATETIME_FORMAT)
			# print(len(feature))
			item["feature"] = feature if len(feature) < 102 else ''
			yield item

		next_url = select.xpath('//a[@id="sogou_next"]/@href').extract_first()
		if next_url:
			next_url = urljoin(response.url, next_url)
			yield scrapy.Request(next_url, dont_filter=True, meta={'dont_redirect': True})

