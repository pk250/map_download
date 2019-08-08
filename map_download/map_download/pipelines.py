# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymysql


class MapDownloadPipeline(object):
    def __init__(self):
        dbparams={
            'host':'192.168.0.122',
            'port':3306,
            'user':'root',
            'password':'liu654321',
            'database':'map',
            'charset':'utf8'
        }
        self.conn=pymysql.connect(**dbparams)
        self.cursor=self.conn.cursor()
        self._sql=None

    def process_item(self, item, spider):
        try:
            result = self.cursor.execute(self.sql,(item['Type_id'],item['Zoom'],item['X'],item['Y'],item['Tile']))
        except Exception as error:
            print("error:{0}\r\n".format(error))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql="""insert into t_map(Type_id,Zoom,X,Y,Tile) VALUES (%s,%s,%s,%s,%s)"""
            return self._sql
        return self._sql