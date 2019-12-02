# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区名
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 几居室，详情是个列表
    rooms = scrapy.Field()
    # 大小，面积
    areas = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 行政区
    district = scrapy.Field()
    # 是否在售
    sales = scrapy.Field()
    # 详情网页链接
    oringin_url = scrapy.Field()

    # 二手房提取项目
class EsfHouseItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区名
    name = scrapy.Field()
    # 几室几厅
    rooms = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 层，中层。。。
    floor = scrapy.Field()
    # 朝向
    direction = scrapy.Field()
    # 年代
    age = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 单价
    unit_price = scrapy.Field()
    # 链接
    link = scrapy.Field()

