# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/16 16:59
# @Function:

from json import loads
from scrapy import Spider, Request
from WeiboSpider.config import TweetConfig
from WeiboSpider.items import TweetItem, LongtextItem


class TweetInfoSpider(Spider):
    name = "tweet_spider"
    allowed_domains = ['m.weibo.cn', 'weibo.com']

    def __init__(self, uid, *args, **kwargs):
        """
        :param uid: same input uid format like user_info_spider
        :param args:
        :param kwargs:
        """
        super(TweetInfoSpider, self).__init__(*args, **kwargs)
        self.__generator = TweetConfig()
        self.__uid_list = list(filter(None, uid.split('|')))

    def start_requests(self):
        """
        generate crawling Request from designated uid.
        :return: Target Request obj.
        """
        for uid in self.__uid_list:
            url = self.__generator.gen_url(uid=uid, page=None)
            yield Request(url=url, dont_filter=True, callback=self._parse_tweet, meta={'uid': uid})

    def parse(self, response, **kwargs):
        """
            Compulsorily implemented due to abstract method.
        """
        pass

    def _parse_tweet(self, response, **kwargs):
        """
            Parse crawled json str and tweet_spider iteratively generate new Request obj.
        """
        weibo_info = loads(response.text)
        data = weibo_info['data']
        page = data['cardlistInfo']['page']
        uid = response.meta['uid']
        if page:
            url = self.__generator.gen_url(uid=uid, page=page)
            yield Request(url=url, dont_filter=True, callback=self._parse_tweet, meta={'uid': uid})
        for card in data['cards']:
            item = TweetItem()
            card['mblog']['uid'] = uid
            item['tweet_info'] = card['mblog']
            # if card['mblog']['isLongText']:
            if True:
                t_id = card['mblog']['id']
                url = self.__generator.gen_url(t_id=t_id)
                longtext_req = Request(
                    url=url, dont_filter=True,
                    callback=self._parse_longtext, meta={'uid': uid, 't_id': t_id}
                )
                yield longtext_req
            yield item

    def _parse_longtext(self, response, **kwargs):
        long_text = loads(response.text)
        item = LongtextItem()
        item['uid'] = response.meta['uid']
        item['t_id'] = response.meta['t_id']
        item['longtext'] = long_text['data']['longTextContent']
        yield item
