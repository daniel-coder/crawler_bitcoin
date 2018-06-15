# -*- coding: utf-8 -*-

from scrapy import Item, Field


class MessageItem(Item):
    """
    比特币新闻
    """

    title = Field()  # 标题
    pic = Field()   # 配图
    time = Field()  # 时间
    up = Field()  # 看多
    down = Field()  # 看空
    url = Field()  # 链接地址
    content = Field()  # 链接地址
