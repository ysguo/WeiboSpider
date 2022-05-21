# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/19 23:45
# @Function:

from WeiboSpider.base import Config


class TweetConfig(Config):
    def __init__(self):
        super(TweetConfig, self).__init__()
        # replace &page to &since_id
        self.__api = {
            'api_0': 'api/container/getIndex?type=__uid&value=',
            'api_1': '&containerid=107603',
            'api_2': '&since_id=',
            'longtext_api': 'statuses/extend?id='
        }
        self.__com_api = {
            'longtext_api': 'ajax/statuses/longtext?id='
        }

    def __call__(self, **kwargs):
        self.gen_url(**kwargs)

    def gen_url(self, **kwargs):
        assert ('uid' in kwargs.keys() and 'page' in kwargs.keys()) or 't_id' in kwargs.keys() or 't_bid' in kwargs.keys(), 'Input Arguments Error!'
        if 'page' in kwargs.keys():
            uid = str(kwargs['uid'])
            page = kwargs['page']
            url = self.url + self.__api['api_0'] + uid + self.__api['api_1'] + uid
            if page:
                url += self.__api['api_2'] + str(page)
            return url
        elif 't_id' in kwargs.keys():
            t_id = str(kwargs['t_id'])
            return self.url + self.__api['longtext_api'] + t_id
        else:
            t_bid = str(kwargs['t_bid'])
            return self.com_url + self.__com_api['longtext_api'] + t_bid
