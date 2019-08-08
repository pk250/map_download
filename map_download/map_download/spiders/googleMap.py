# -*- coding: utf-8 -*-
import scrapy


class GooglemapSpider(scrapy.Spider):
    name = 'googleMap'
    allowed_domains = ['mt1.google.cn']
    start_urls = ['http://mt1.google.cn/']

    def parse(self, response):
        pass
