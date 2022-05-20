from scrapy.cmdline import execute


if __name__ == '__main__':
    spider_cmd = "scrapy crawl weibo_spider -a uid=user0|user2"
    execute(spider_cmd.split())


