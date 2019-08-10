# -*- coding: utf-8 -*-
from urllib import parse
from urllib.parse import urljoin

import scrapy
import math

from map_download.items import MapDownloadItem


class GooglemapSpider(scrapy.Spider):
    name = 'googleMap'
    allowed_domains = ['mt1.google.cn']
    start_urls = ['http://mt1.google.cn/']

    def parse(self, response):
        url=parse.parse_qs(response.url)
        Tile=response.body
        # TODO 去水印
        if url['lyrs'][0]=="s@218":
            Type_id = 47626774
        else:
            Type_id = 1024577166
        Zoom=url['z'][0]
        X=url['x'][0]
        Y=url['y'][0]
        item=MapDownloadItem(
            Type_id=Type_id,
            Zoom=Zoom,
            X=X,
            Y=Y,
            Tile=Tile
        )
        print("Type_id={0},Zoom={1},X={2},Y={3}\r\n".format(Type_id,Zoom,X,Y))
        yield item
        pass

    # 拼接url值
    def getUrl(self,mapType,x,y,z):
         urlformat="vt/imgtp=png32&lyrs={0}&hl=zh-CN&gl=cn&x={1}&y={2}&z={3}&s=Galil"
         return urlformat.format(mapType,x,y,z)
    # 经纬度转换为瓦片值
    def deg2num(self,lat_deg, lon_deg, zoom):
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return (xtile, ytile)

    def start_requests(self):
        for zoom in range(20):
            # TODO 地图选择区域
            lefttop = self.deg2num(50, 70, zoom)
            rightbottom = self.deg2num(12, 145, zoom)
            for x in range(lefttop[0],rightbottom[0]):
                for y in range(lefttop[1],rightbottom[1]):
                    for type in range(2):
                        if type==0:
                            yield scrapy.Request(urljoin(self.start_urls[0], self.getUrl("s@218", x, y, zoom)),
                                             callback=self.parse)
                        else:
                            yield scrapy.Request(urljoin(self.start_urls[0], self.getUrl("h@218", x, y, zoom)),
                                                 callback=self.parse)