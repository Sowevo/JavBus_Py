# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MainItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 编号
    code = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 码
    censored = scrapy.Field()
    # 演员,多个
    stars = scrapy.Field()
    # 发行时间
    release_date = scrapy.Field()
    # 持续时间
    duration = scrapy.Field()
    # 导演
    director = scrapy.Field()
    # 制作商
    maker = scrapy.Field()
    # 发行商
    publisher = scrapy.Field()
    # 标签
    tags = scrapy.Field()
    # 封面
    cover = scrapy.Field()
    # 预览图
    previews = scrapy.Field()
    # 系列
    series = scrapy.Field()
    # 磁链
    magnets = scrapy.Field()
    # 更新时间
    update_time = scrapy.Field()
