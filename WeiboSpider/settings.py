# -*- coding: utf-8 -*-
# Scrapy settings for WeiboSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'WeiboSpider'

SPIDER_MODULES = ['WeiboSpider.spiders']
NEWSPIDER_MODULE = 'WeiboSpider.spiders'

LOG_FILE = "WeiboSpider.log"
LOG_LEVEL = "INFO"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 64
CONCURRENT_REQUESTS_PER_IP = 0

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#    'Accept-Language': 'zh',
#}

#DEFAULT_REQUEST_HEADERS = {
#    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#    'Accept-Language': 'zh-CN,zh;q=0.9',
#    'Cookie': 'SINAGLOBAL=1108923899813.7717.1637807606934; UOR=,,www.baidu.com; ariaDefaultTheme=default; ariaFixed=true; ariaScale=1; ariaBigsrc=false; ariaReadtype=1; ariaMouseten=null; ariaStatus=false; ULV=1652930164990:11:4:2:7922061087235.483.1652930164925:1652867655325; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhREBuPIwBoTa75z632Q8lz5JpX5KMhUgL.FoqNS0n7SK.c1hM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcS0MReh-4SonN; ALF=1684555689; SSOLoginState=1653019689; SCF=Ah5BB6-7ijH27iamVozk-9ubzPTmXWY05HUIbLsGtMolrHzfGCAc99S7w2iBL13RRKctsJLOZZiTE9ZsAsn8IBE.; SUB=_2A25Pg2R6DeRhGeBJ7FoR9SfKwzuIHXVs-dKyrDV8PUNbmtAfLRnDkW9NRiNheAmgzALUDlPQDgiA1WvAudL225ph; XSRF-TOKEN=qTRfK5zjSg8IlyjlhrvHK3KV; WBPSESS=MBqW2JtgrXOE05BwrlA9SlV6vWcy8IuvvEi9wuZetVLNStYMEWF9ShuIFYE12L21zZNB54tSBQv1flctWQrLSwDmUGTpOGMu2-m952UyhW-opdJSr4Wh0twMyLo5NomXwrZdLXZ6FPCmqU9kKPznyQ=='
#}

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh',
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
    'WeiboSpider.middlewares.InitialMiddleware': 50,
    'WeiboSpider.middlewares.FakeUserAgentMiddleware': 100,
    'WeiboSpider.middlewares.ProxyMiddleware': None,  # 150
    'WeiboSpider.middlewares.RetryMiddleware': 250  # 250
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'WeiboSpider.pipelines.UserInfoPipeline': 100,
    'WeiboSpider.pipelines.TweetInfoPipeline': 150,  # 150
    'WeiboSpider.pipelines.LongtextPipeline': 200,
    'WeiboSpider.pipelines.ErrorPipeline': 250
}

# Custom Option
# To get proxy, each proxy form like "https://xxx.xxx.xxx:xxxx/"
PROXY_URL = ''

# The max retry times when crawling failed
MAX_RETRY_TIME = 3

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'WeiboSpider.middlewares.WeiboSpiderSpiderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
