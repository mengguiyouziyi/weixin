# coding:utf-8
import os
import sys
from rediscluster import StrictRedisCluster
from scrapy.cmdline import execute

base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(base_path)

startup_nodes = [{"host": "172.29.237.209", "port": "7000"},
                 {"host": "172.29.237.209", "port": "7001"},
                 {"host": "172.29.237.209", "port": "7002"},
                 {"host": "172.29.237.214", "port": "7003"},
                 {"host": "172.29.237.214", "port": "7004"},
                 {"host": "172.29.237.214", "port": "7005"},
                 {"host": "172.29.237.215", "port": "7006"},
                 {"host": "172.29.237.215", "port": "7007"},
                 {"host": "172.29.237.215", "port": "7008"}]

rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

execute(['scrapy', 'crawl', 'search'])
