# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/16 16:59
# @Function:

from json import loads, JSONDecodeError
from scrapy import Request
import logging
from WeiboSpider.base import BaseSpider
from WeiboSpider.config import TweetConfig
from WeiboSpider.items import TweetItem, LongtextItem


class TweetInfoSpider(BaseSpider):
    name = "tweet_spider"

    def __init__(self, uid, *args, **kwargs):
        """
            The `tweet_spider` was designed to crawl user's tweets.
            It firstly inherits the `BaseSpider` class, and implements `_parse_tweet` and `_parse_longtext` function to
            extract user's tweets or longtext respectively.
        """
        super(TweetInfoSpider, self).__init__(uid, *args, **kwargs)
        self._t_generator = TweetConfig()

    def start_requests(self):
        """
        generate crawling Request from designated uid.
        :return: Target Request obj.
        """
        uid_list = self.get_uid_list(self.uid)
        for uid in uid_list:
            url = self._t_generator.gen_url(uid=uid, page=None)
            yield Request(url=url, dont_filter=True, callback=self._parse_tweet, errback=self.parse_err,
                          meta={'uid': uid, 'last_page': 0})

    def _parse_tweet(self, response, **kwargs):
        """
            Parse crawled json str and tweet_spider iteratively generate new Request obj.
        """

        weibo_info = loads(response.text)
        data = weibo_info['data']
        # page = data['cardlistInfo']['page']
        try:
            page = data['cardlistInfo']['since_id']
        except KeyError:
            logging.info("Maybe KeyError: 'since_id', the spider finish the task he could do")
            page = None
        uid = response.meta['uid']
        last_page = response.meta['last_page']
        if last_page == 0:
            if page is not None and int(page) != last_page:
                url = self._t_generator.gen_url(uid=uid, page=page)
                yield Request(url=url, dont_filter=True, callback=self._parse_tweet, errback=self.parse_err,
                              meta={'uid': uid, 'last_page': last_page})
        elif last_page > 1:
            if page is not None and int(page) != last_page:
                print(last_page)
                url = self._t_generator.gen_url(uid=uid, page=page)
                yield Request(url=url, dont_filter=True, callback=self._parse_tweet, errback=self.parse_err,
                              meta={'uid': uid, 'last_page': int(last_page-1)})
        else:
            pass

        for card in data['cards']:
            item = TweetItem()
            card['mblog']['uid'] = uid
            item['tweet_info'] = card['mblog']
            if card['mblog']['isLongText']:
                t_id = card['mblog']['id']
                t_bid = card['mblog']['bid']
                url = self._t_generator.gen_url(t_id=t_id)
                url_com = self._t_generator.gen_url(t_bid=t_bid)
                try:
                    longtext_req = Request(
                        url=url, dont_filter=True, errback=self.parse_err,
                        callback=self._parse_longtext, meta={'uid': uid, 't_id': t_id, 't_bid': t_bid}
                    )
                    yield longtext_req
                except Exception as e:
                    print("try .com")
                    longtext_req = Request(
                        url=url_com, dont_filter=True, errback=self.parse_err,
                        callback=self._parse_longtext, meta={'uid': uid, 't_id': t_id, 't_bid': t_bid}
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

    def parse(self, response, **kwargs):
        """
            Compulsorily implemented due to abstract method.
        """
        pass
