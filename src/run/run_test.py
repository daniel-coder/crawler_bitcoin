# -*- coding: utf-8 -*-

from os import path as os_path
from sys import path as sys_path

sys_path.append(os_path.dirname(os_path.dirname(os_path.dirname(os_path.abspath(__file__)))))

from src.run.utils import run_scrapy_spider

if __name__ == '__main__':
    from src.spiders.test_spider import TestSpider, TestJsSpider, \
        TestPhantomJSSpider, TestHeadlessChromeSpider

    run_scrapy_spider([TestSpider,
                       TestPhantomJSSpider,
                       TestHeadlessChromeSpider,
                       TestJsSpider,
                       ])
