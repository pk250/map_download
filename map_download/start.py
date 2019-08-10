from scrapy import cmdline

# TODO 添加地图服务

cmdline.execute("scrapy crawl googleMap --nolog -o log.csv".split())