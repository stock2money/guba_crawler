# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GubaReviewItem(scrapy.Item):
    # define the fields for your item here like:
    # 标题
    title = scrapy.Field()
    # 详情
    detail = scrapy.Field()
    # 发表时间
    time = scrapy.Field()
    # 原链接
    href = scrapy.Field()
    # 股票代码
    code = scrapy.Field()
    # 发表者
    author = scrapy.Field()
    # 情感
    emotion = scrapy.Field()
    # 类型 - 0 - news or 1 - stock
    infoType = scrapy.Field()