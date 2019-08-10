# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from pymysql.cursors import DictCursor
import pymysql
from twisted.enterprise import adbapi

from map_download import settings


class MapDownloadPipeline(object):
    def __init__(self):
        dbparams={
            'host':settings.MYSQL_HOST,
            'port':settings.MYSQL_PORT,
            'user':settings.MYSQL_USER,
            'password':settings.MYSQL_PASSWD,
            'database':settings.MYSQL_DBNAME,
            'charset':'utf8'
        }
        self.dbpool=adbapi.ConnectionPool('pymysql',**dbparams)
        # self.conn=pymysql.connect(**dbparams)
        # self.cursor=self.conn.cursor()
        self._sql=None

    def process_item(self, item, spider):
        defer=self.dbpool.runInteraction(self.insert_item,item)
        defer.addErrback(self.handle_error,item,spider)
        return item
    # 捕获异常
    def handle_error(self,error,item,spider):
        return
        #print("error:{0}\r\n".format(error))
    # 插入数据
    def insert_item(self,cursor,item):
        Type_id,Zoom,X,Y,Tile=item.values()
        cursor.execute(self.sql,(Type_id,Zoom,X,Y,Tile))

    @property
    def sql(self):
        if not self._sql:
            self._sql="""insert into t_map(Type_id,Zoom,X,Y,Tile) VALUES (%s,%s,%s,%s,%s)"""
            return self._sql
        return self._sql