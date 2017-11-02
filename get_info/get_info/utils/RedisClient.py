# -*- coding: utf-8 -*-
# !/usr/bin/env python

'''
self.key为Redis中的一个field
2017/4/17 修改pop
'''
import sys
from rediscluster import StrictRedisCluster


class RedisClient(object):
	def __init__(self, key, startup_nodes):
		"""
		init cluster
		"""
		self.key = key
		self.conn = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

	def hdel(self, field):
		"""
		delete an item
		:param field:
		:return:
		"""
		self.conn.hdel(self.key, field)

	def hexists(self, field):
		"""
		判断 key 中是否含有 field
		:param field:
		:return:
		"""
		return self.conn.hexists(self.key, field)

	def hget(self, field):
		"""
		返回key中指定 field 中的 value
		:param field:
		:return:
		"""
		value = self.conn.hget(self.key, field)
		if isinstance(value, bytes):
			return value.decode('utf-8')
		else:
			return value if value else None

	def hgetall(self):
		"""
		获取 {filed: value, field1: value1....}
		:return:
		"""
		all_dict = self.conn.hgetall(self.key)
		if not all_dict:
			return
		elif sys.version_info.major == 3:
			return {field.decode('utf-8'): value.decode('utf-8') for field, value in all_dict.items()}
		else:
			return all_dict

	def hkeys(self):
		"""
		获取key中所有field
		:return:
		"""
		field = self.conn.hkeys(self.key)
		if isinstance(field, bytes):
			return field.decode('utf-8')
		else:
			return field if field else None

	def hlen(self):
		"""
		获取所有 filed 数量
		:return:
		"""
		return self.conn.hlen(self.key)

	def hset(self, field, value):
		"""
		设置 field: value
		:param field:
		:param value:
		:return:
		"""
		self.conn.hset(self.key, field, value)

	def hvals(self):
		"""
		获取所有values
		:return:
		"""
		values = self.conn.hvals(self.key)
		if not values:
			return
		elif sys.version_info.major == 3:
			return [value.decode('utf-8') for value in values]
		else:
			return values

	def change_key(self, key):
		"""
		替换 key
		:param key:
		:return:
		"""
		self.key = key

	# ===============================================
	def blpop(self, timeout):
		self.conn.blpop(self.key, timeout=timeout)

	def brpop(self, timeout):
		self.conn.brpop(self.key, timeout=timeout)

	def brpoplpush(self, dst, timeout):
		self.conn.brpoplpush(self.key, dst=dst, timeout=timeout)

	def lindex(self, i):
		self.conn.lindex(self.key, index=i)

	def llen(self):
		self.conn.llen(self.key)

	def lpop(self):
		self.conn.lpop(self.key)

	def lpush(self):
		self.conn.lpush(self.key)

	def lrange(self, start, stop):
		self.conn.lrange(self.key, start, stop)

	def lset(self, i, value):
		self.conn.lset(self.key, index=i, value=value)

	def rpop(self):
		self.conn.rpop(self.key)

	def rpoplpush(self, dst):
		self.conn.rpoplpush(self.key, dst=dst)

	def rpush(self, value):
		self.conn.rpush(self.key, value)

	# ===============================================


if __name__ == '__main__':
	startup_nodes = [{"host": "172.29.237.209", "port": "7000"},
	                 {"host": "172.29.237.209", "port": "7001"},
	                 {"host": "172.29.237.209", "port": "7002"},
	                 {"host": "172.29.237.214", "port": "7003"},
	                 {"host": "172.29.237.214", "port": "7004"},
	                 {"host": "172.29.237.214", "port": "7005"},
	                 {"host": "172.29.237.215", "port": "7006"},
	                 {"host": "172.29.237.215", "port": "7007"},
	                 {"host": "172.29.237.215", "port": "7008"}]

	conn = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
	conn.lpush('nihao', 'dajiahao', 'shuihao')
