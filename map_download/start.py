from scrapy import cmdline

cmdline.execute("scrapy crawl googleMap --nolog -o log.csv".split())