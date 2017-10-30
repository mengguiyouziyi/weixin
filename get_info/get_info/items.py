# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GetInfoItem(scrapy.Item):
    # define the fields for your item here like:
    pub_name = scrapy.Field()
    pic_url = scrapy.Field()
    weixin = scrapy.Field()
    feature = scrapy.Field()
    comp = scrapy.Field()
    url_dt = scrapy.Field()
    # crawlTime = scrapy.Field()
