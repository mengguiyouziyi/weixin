# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import base64
from random import choice
from get_info.utils.RedisClient import RedisClient
from scrapy.exceptions import IgnoreRequest
import time

# 代理服务器
proxyServer = "http://proxy.abuyun.com:9020"

# 百科的账号
# 1
proxyUser = "H3OTY534E26645SD"
proxyPass = "685BA207E1946E6C"

# 2
# proxyUser = "H689K6HN8Z46666D"
# proxyPass = "3E0DCB86C35C5504"

# 3
# proxyUser = "H51N0CWJLZX5981D"
# proxyPass = "24606F3C6193A99D"

# 4
# proxyUser = "HL6O95146U41Z61D"
# proxyPass = "8F2622D2D6A1A73F"

# 5
# proxyUser = "HI4Z5PI5D1Y44S2D"
# proxyPass = "5D698C9C15113ACE"

# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


class ProxyMiddleware(object):
	def process_request(self, request, spider):
		if spider.name == 'search':
			request.meta["proxy"] = proxyServer
			request.headers["Proxy-Authorization"] = proxyAuth
		elif spider.name == 'detail':
			redis_con = RedisClient('useful_proxy', 'a027.hb2.innotree.org', 6379)
			thisip = redis_con.get()
			if not thisip:
				raise IgnoreRequest
			print("this is ip:" + thisip)
			request.meta["proxy"] = "http://" + thisip
		else:
			raise IgnoreRequest


class RetryMiddleware(object):
	def process_response(self, request, response, spider):
		if response.status in [429, 302]:
			# print('status:%s~~~retring~~~title:%s' % (str(response.status), response.url))
			return request.copy()
		# elif '验证码' in response.text:
		# 	print('验证码：：：status:%s~~~retring~~~title:%s' % (str(response.status), response.url))
		# 	return request.copy()
		else:
			return response

	def process_exception(self, request, exception, spider):
		return request.copy()


class RotateUserAgentMiddleware(object):
	"""Middleware used for rotating user-agent for each request"""

	def __init__(self, agents):
		self.agents = agents

	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings.get('USER_AGENT_CHOICES', []))

	def process_request(self, request, spider):
		request.headers.setdefault('User-Agent', choice(self.agents))
