# -*- coding: utf-8 -*-
# !/usr/bin/env python

'''
self.key为Redis中的一个field
2017/4/17 修改pop
'''

# import json
# import random
# import redis
import sys
from rediscluster import StrictRedisCluster


class RedisClient(object):
	"""
	Reids client
	"""

	# def __init__(self, key, host, port=6379, db=0):
	# 	"""
	# 	init single
	# 	:param key:
	# 	:param host:
	# 	:param port:
	# 	:param db:
	# 	"""
	# 	self.key = key
	# 	pool = redis.ConnectionPool(host=host, port=port, db=db)
	# 	self.conn = redis.StrictRedis(connection_pool=pool, decode_responses=True)

	def __init__(self, key, startup_nodes):
		"""
		init cluster
		:param key:
		:param host:
		:param port:
		:param db:
		"""
		self.key = key
		self.conn = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

	def delete(self, field):
		"""
		delete an item
		:param field:
		:return:
		"""
		self.conn.hdel(self.key, field)

	# self.conn.srem(self.key, value)

	def hexists(self, field):
		"""
		判断 key 中是否含有 field
		:param field:
		:return:
		"""
		return self.conn.hexists(self.key, field)

	def get_value(self, field):
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

	def get_field_value(self):
		"""
		获取 {filed: value, field1: value1....}
		:return:
		"""
		# return self.conn.hgetall(self.key).fields()
		# python3 redis返回bytes类型,需要解码
		all_dict = self.conn.hgetall(self.key)
		if not all_dict:
			return
		elif sys.version_info.major == 3:
			return {field.decode('utf-8'): value.decode('utf-8') for field, value in all_dict.items()}
		else:
			return all_dict
		# return self.conn.smembers(self.key)

	def get_fields(self):
		"""
		获取key中所有field
		:return:
		"""
		field = self.conn.hkeys(self.key)
		if isinstance(field, bytes):
			return field.decode('utf-8')
		else:
			return field if field else None

	def get_len(self):
		"""
		获取所有 filed 数量
		:return:
		"""
		return self.conn.hlen(self.key)

	def set_field_value(self, field, value):
		"""
		设置 field: value
		:param field:
		:param value:
		:return:
		"""
		self.conn.hset(self.key, field, value)

	def get_values(self):
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

	# def get(self):
	# 	"""
	# 	get random result
	# 	:return:
	# 	"""
	# 	field_value = self.conn.hgetall(self.key)
	# 	# return random.choice(field.fields()) if field else None
	# 	# field.fields()在python3中返回dict_fields，不支持index，不能直接使用random.choice
	# 	# 另：python3中，redis返回为bytes,需要解码
	# 	rfield = random.choice(list(field_value.keys())) if field_value else None
	# 	if isinstance(rfield, bytes):
	# 		return rfield.decode('utf-8')
	# 	else:
	# 		return rfield
	# 		# return self.conn.srandmember(key=self.key)
	#
	# def put(self, field):
	# 	"""
	# 	put an  item
	# 	:param value:
	# 	:return:
	# 	"""
	# 	field = json.dumps(field) if isinstance(field, (dict, list)) else field
	# 	return self.conn.hincrby(self.key, field, 1)
	# 	# return self.conn.sadd(self.key, value)
	#
	# def pop(self):
	# 	"""
	# 	pop an item
	# 	:return:
	# 	"""
	# 	field = self.get()
	# 	if field:
	# 		self.conn.hdel(self.key, field)
	# 	return field
	# 	# return self.conn.spop(self.key)
	#
	#
	#
	# def incfield(self, field, value):
	# 	self.conn.hincrby(self.key, field, value)
	#
	#
	#
	# def get_status(self):
	# 	return self.conn.hlen(self.key)
	# 	# return self.conn.scard(self.key)


if __name__ == '__main__':
	# redis_con = RedisClient('comp_gaoxin_only_id', 'a027.hb2.innotree.org', 6379)
	# print(redis_con.getAll())
	# redis_con.put('abc')
	# redis_con.put('123')
	# redis_con.put('123.115.235.221:8800')
	# redis_con.put(['123', '115', '235.221:8800'])
	# print(redis_con.getAll())
	# redis_con.delete('abc')
	# print(redis_con.getAll())

	# print(redis_con.getAll())
	# redis_con.changeTable('raw_proxy')
	# redis_con.pop()

	# redis_con.put('132.112.43.221:8888')
	# redis_con.changeTable('proxy')
	# print(redis_con.get_status())
	# print(redis_con.getAll())

	startup_nodes = [{"host": "172.29.237.209", "port": "7000"},
	                 {"host": "172.29.237.209", "port": "7001"},
	                 {"host": "172.29.237.209", "port": "7002"},
	                 {"host": "172.29.237.214", "port": "7003"},
	                 {"host": "172.29.237.214", "port": "7004"},
	                 {"host": "172.29.237.214", "port": "7005"},
	                 {"host": "172.29.237.215", "port": "7006"},
	                 {"host": "172.29.237.215", "port": "7007"},
	                 {"host": "172.29.237.215", "port": "7008"}]

