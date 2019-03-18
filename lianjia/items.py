# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    newDiskID =scrapy.Field()
    area = scrapy.Field()
    plate=scrapy.Field()
    address = scrapy.Field()
    diskName =scrapy.Field()
    totalPrice = scrapy.Field()
    averagePrice =scrapy.Field()
    acreage = scrapy.Field()
    roomDetail =scrapy.Field()
    allFloor =scrapy.Field()
    floor =scrapy.Field()
    floorLevel=scrapy.Field()
    direction = scrapy.Field()
    houseType = scrapy.Field()
    decoration = scrapy.Field()
    builtYear = scrapy.Field()
    fromWebSite = scrapy.Field()
    url = scrapy.Field()
    crawlDate = scrapy.Field()
    type = scrapy.Field()
    jingwei=scrapy.Field()
    listingTime=scrapy.Field()
    pass