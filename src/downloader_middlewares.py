# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

# from scrapy.downloadermiddlewares.robotstxt import RobotsTxtMiddleware
# from scrapy.downloadermiddlewares.httpauth import HttpAuthMiddleware
# from scrapy.downloadermiddlewares.downloadtimeout import DownloadTimeoutMiddleware
# from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
# from scrapy.downloadermiddlewares.retry import RetryMiddleware
# from scrapy.downloadermiddlewares.defaultheaders import DefaultHeadersMiddleware
# from scrapy.downloadermiddlewares.redirect import MetaRefreshMiddleware
# from scrapy.downloadermiddlewares.httpcompression import HttpCompressionMiddleware
# from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
# from scrapy.downloadermiddlewares.cookies import CookiesMiddleware
# from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
# from scrapy.downloadermiddlewares.chunked import ChunkedTransferMiddleware
# from scrapy.downloadermiddlewares.stats import DownloaderStats
# from scrapy.downloadermiddlewares.httpcache import HttpCacheMiddleware

from urllib.parse import urlparse, urlunparse

from src.spiders.spider_classes import JsRequestSpider
from src.utils.web_utils import get_one_ua


class RandomUserAgentDownloaderMiddleware(object):
    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', get_one_ua())


class JsDownloaderMiddleware(object):
    def process_request(self, request, spider):
        if isinstance(spider, JsRequestSpider):
            url = request.url
            if not url.startswith("js://"):
                new_request = request.replace(url=urlunparse(("js",) + urlparse(url)[1:]))

                meta = new_request.meta
                meta["Original_Url"] = url
                if "JS_Finish_Xpath" not in meta:
                    meta["JS_Finish_Xpath"] = spider.js_finish_xpath

                return new_request
