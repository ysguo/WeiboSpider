# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/17 1:09
# @Function:

from abc import ABC, abstractmethod


class Config(ABC):
    def __init__(self):
        self.url = "https://m.weibo.cn/"
        self.com_url = "https://weibo.com/"

    @abstractmethod
    def gen_url(self, *args, **kwargs):
        pass
