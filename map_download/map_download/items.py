# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MapDownloadItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Type_id = scrapy.Field()
    Zoom = scrapy.Field()
    X = scrapy.Field()
    Y = scrapy.Field()
    Tile = scrapy.Field()
