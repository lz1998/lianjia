# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import time
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy.orm import sessionmaker, mapper, clear_mappers

engine = None
Session = None
session = None
#mysql+mysqldb://root@localhost:3306/blog?charset=utf8
metadata = MetaData()
t = Table("000000", metadata,
          Column("id", String(20), primary_key=True),  # md5作为id
          Column("newDiskID", Integer),
          Column("area", String(10)),
          Column("plate", String(10)),
          Column("address", String(10)),
          Column("diskName", String(255)),
          Column("totalPrice", Integer),
          Column("averagePrice", Integer),
          Column("acreage", Float),
          Column("roomDetail", String(50)),
          Column("allFloor", Integer),
          Column("floor", Integer),
          Column("floorLevel", String(10)),
          Column("direction", String(10)),
          Column("houseType", String(10)),
          Column("decoration", String(10)),
          Column("builtYear", Date),
          Column("fromWebSite", String(10)),
          Column("url", String(255)),
          Column("crawlDate", Date),
          Column("type", String(255)),
          Column("jingwei", String(31))
          )


class HouseDetail(object):
    def __init__(self):
        self.id = None
        self.newDiskID = None
        self.area = None
        self.plate = None
        self.address = None
        self.diskName = None
        self.totalPrice = None
        self.averagePrice = None
        self.acreage = None
        self.roomDetail = None
        self.allFloor = None
        self.floor = None
        self.floorLevel = None
        self.direction = None
        self.houseType = None
        self.decoration = None
        self.builtYear = None
        self.fromWebSite = None
        self.url = None
        self.crawlDate = None
        self.type = None
        self.jingwei = None


class LianjiaPipeline(object):
    f = None

    def open_spider(self, spider):
        global engine, Session
        engine = create_engine('mysql+pymysql://housing:housing@101.132.154.2:3306/House_OnSale', encoding='utf-8', echo=False)
        Session = sessionmaker(bind=engine)
        pass

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
        print("ok")

    def process_item(self, item, spider):
        # print("get an item")
        # for key in item:
        #     print(key + ":" + str(item[key]))
        # print("-------------------------")
        try:
            tableName = item['crawlDate'].strftime("%Y%m")
            self.saveData(item, tableName)
        except Exception as e:
            print(e)

    def saveData(self, item, tableName):
        # 设置修改的表名
        t.name = tableName
        if not t.exists(bind=engine):
            t.create(bind=engine)
        clear_mappers()
        mapper(HouseDetail, t)
        # print(111)
        houseDetail = HouseDetail()
        for key in item:
            if hasattr(houseDetail, key):
                setattr(houseDetail, key, item[key])
        global Session
        session = Session()
        session.add(houseDetail)
        session.commit()
