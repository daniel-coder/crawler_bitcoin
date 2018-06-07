# -*- coding: utf-8 -*-

from scrapy import Item, Field


class NewsItem(Item):
    """
    比特币新闻
    """

    title = Field()  # 标题
    time = Field()  # 时间
    url = Field()  # 链接地址
    content = Field()  # 链接地址
