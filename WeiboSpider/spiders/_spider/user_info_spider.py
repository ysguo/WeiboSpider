# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/16 16:58
# @Function:

import json
from scrapy import Spider
from WeiboSpider.items import UserInfoItem
from ..config.UserInfoConfig import UserInfoConfig


class UserInfoSpider(Spider):
    name = "user_info_spider"
    allowed_domains = ['m.weibo.cn', "weibo.com", "weibo.cn"]

    def __init__(self, uid: str, *args, **kwargs):
        super(UserInfoSpider, self).__init__(*args, **kwargs)
        self.__generator = UserInfoConfig()

    def start_requests(self):
        # how to get target uid? This is a question. Sleep!
        for _ in self.uid.split('|'):
            print(_)

    def parse(self, response, **kwargs):
        pass

    def _parse_profile(self, response):
        pass
