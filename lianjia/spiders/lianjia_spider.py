# -*- coding: utf-8 -*-
import hashlib

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from ..items import LianjiaItem
import time
import datetime
import re


class LianjiaSpiderSpider(scrapy.Spider):
    name = 'lianjia_spider'
    allowed_domains = ['sh.lianjia.com']
    start_urls = ['http://sh.lianjia.com/ershoufang/']
    cnt = 0

    def parse(self, response):
        sel = Selector(response=response)
        urls = sel.xpath("//div[@class='position']//div[@data-role='ershoufang']/div[1]/a/@href").extract()
        for url in urls:
            url = "https://sh.lianjia.com%s" % url
            yield Request(url=url, callback=self.parse_a, dont_filter=True)

    def parse_a(self, response):
        sel = Selector(response=response)
        urls = sel.xpath("//div[@class='position']//div[@data-role='ershoufang']/div[2]/a/@href").extract()
        for url in urls:
            url = "https://sh.lianjia.com%s" % url
            yield Request(url=url, callback=self.parse_b_page, dont_filter=True)

    def parse_b_page(self, response):
        sel = Selector(response=response)
        page_data = eval(sel.xpath("//div[@class='page-box house-lst-page-box']/@page-data").extract()[0])
        for page in range(1, page_data['totalPage'] + 1):
            url = "%spg%s/" % (response.url, page)
            yield Request(url=url, callback=self.parse_b, dont_filter=True)

    def parse_b(self, response):
        sel = Selector(response=response)
        urls = sel.xpath("//ul[@class='sellListContent']/li/a/@href").extract()
        for url in urls:
            # print(url)
            yield Request(url=url, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        item = LianjiaItem()
        # item=[]
        sel = Selector(response)
        # print(1)

        diskName = sel.xpath("//div[@class='communityName']/a[1]/text()").extract()[0]  # 小区名称
        total_price = sel.xpath("//span[@class='total']/text()").extract()[0]  # 总价
        aver_price = sel.xpath('//div[@class="unitPrice"]/span[@class="unitPriceValue"]/text()').extract()[0]  # 均价
        acreage = sel.xpath("//div[@class='area']/div[@class='mainInfo']/text()").extract()[0]  # 面积
        direction = sel.xpath("//div[@class='type']/div[@class='mainInfo']/text()").extract()[0]  # 朝向
        area = sel.xpath("//div[@class='areaName']//a/text()").extract()[0]  # 区
        plate = sel.xpath("//div[@class='areaName']//a/text()").extract()[1]  # 地址
        decoration = sel.xpath("//div[@class='base']/div[@class='content']/ul//li[9]/text()").extract()[0]  # 装修情况
        allFloor = sel.xpath("//div[@class='base']/div[@class='content']/ul/li[2]/text()").extract()[0][6:8]  # 楼层高度
        floorLevel = sel.xpath("//div[@class='base']/div[@class='content']/ul/li[2]/text()").extract()[0][0:3]  # 楼层状态
        roomDetail = sel.xpath("//div[@class='base']/div[@class='content']/ul/li[1]/text()").extract()[0]  # 房屋结构
        houseType = sel.xpath("//div[@class='content']/ul/li[4]/span[2]/text()").extract()[0]  # 房屋类型
        listingtime = sel.xpath("//div[@class='content']/ul/li[1]/span[2]/text()").extract()[0]  # 挂牌时间
        last_transactin = sel.xpath("//div[@class='content']/ul/li[3]/span[2]/text()").extract()[0]  # 建筑年代
        builtYear = sel.xpath("//div[@class='area']/div[@class='subInfo']/text()").extract()[0][0:4]
        if builtYear == "未知年建":
            builtYear = "2000"

        try:
            transportation = sel.xpath("//div[@class='areaName']/a/text()").extract()[0]
        except Exception:
            transportation = '无'

        # print(transportation)

        # resblockPosition:'121.497997,31.226867'
        jingwei = re.search("resblockPosition:'([^']+)'", response.text).group(1)
        url = response.url
        fromWebSite = '链家网'
        # crawlDate = time.strftime("%Y-%m-%d")
        item['id'] = hashlib.new('md5', url.encode('utf-8')).hexdigest()
        item['newDiskID'] = 0
        item['area'] = area
        item['address'] = ""
        item['plate'] = plate
        item['diskName'] = diskName
        item['totalPrice'] = total_price + "0000"
        item['averagePrice'] = aver_price
        item['acreage'] = acreage.replace("平", "").replace("米", "")
        item['roomDetail'] = roomDetail
        item['allFloor'] = allFloor.replace("层", "")
        item['floor'] = ""
        item['floorLevel'] = floorLevel
        item['direction'] = direction
        item['houseType'] = houseType
        item['decoration'] = decoration
        item['builtYear'] = datetime.datetime.strptime(builtYear, "%Y").date()
        item['fromWebSite'] = fromWebSite
        item['url'] = url
        item['crawlDate'] = datetime.datetime.now().date()
        item['type'] = houseType
        item['jingwei']=jingwei
        item['listingTime'] = listingtime
        self.cnt += 1

        if self.cnt % 100 == 0:
            print("已爬取", self.cnt, "条信息")
        yield item
