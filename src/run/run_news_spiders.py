# -*- coding: utf-8 -*-

from os import path as os_path
from sys import path as sys_path

sys_path.append(os_path.dirname(os_path.dirname(os_path.dirname(os_path.abspath(__file__)))))

from src.run.utils import run_scrapy_spider

if __name__ == '__main__':
    from src.spiders.news_spiders.btc8 import Btc8Spider
    from src.spiders.news_spiders.bitkan import BitkanSpider

    run_scrapy_spider([BitkanSpider,
                      ])
