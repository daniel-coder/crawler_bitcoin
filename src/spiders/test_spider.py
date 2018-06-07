# -*- coding: utf-8 -*-

from scrapy import Spider
from scrapy.http import HtmlResponse

from src.spiders.spider_classes import WebdriverSpider, JsRequestSpider, \
    PhantomJSWebdriverSpider, HeadlessChromeWebdriverSpider


class BaseTestSpider(Spider):
    custom_settings = {
        'LOG_LEVEL': "WARNING",
    }


class TestSpider(BaseTestSpider):
    name = "TEST_SPIDER"
    allowed_domains = ["baidu.com"]
    start_urls = ["https://www.baidu.com/"]

    def parse(self, response):
        self.logger.warning(response.xpath("//a/text()").extract_first("Non found!!!"))


class TestWebDriverSpider(BaseTestSpider, WebdriverSpider):
    allowed_domains = ["xueqiu.com"]
    start_urls = ["https://xueqiu.com/S/SH601398/GBJG"]

    def parse(self, response):
        url = response.url
        table_xpath_str = "//table[contains(@class,'dataTable')]"
        try:
            driver = self.load_page_by_webdriver(url, table_xpath_str)
            html_body = driver.page_source
        finally:
            driver.quit()

        response = HtmlResponse(url, encoding="utf-8", body=html_body)
        self.logger.warning(response.xpath(table_xpath_str + "/tbody/tr").extract_first("Non found!!!"))


class TestPhantomJSSpider(TestWebDriverSpider, PhantomJSWebdriverSpider):
    name = "TEST_PHANTOMJS_SPIDER"


class TestHeadlessChromeSpider(TestWebDriverSpider, HeadlessChromeWebdriverSpider):
    name = "TEST_HEADLESS_CHROME_SPIDER"


class TestJsSpider(BaseTestSpider, JsRequestSpider):
    name = "TEST_JS_SPIDER"
    allowed_domains = ["xueqiu.com"]
    start_urls = ["https://xueqiu.com/S/SH601398/GBJG"]

    def __init__(self, *args, **kwargs):
        self.table_xpath_str = "//table[contains(@class,'dataTable')]"
        super().__init__(*args,
                         js_finish_xpath=self.table_xpath_str,
                         **kwargs)

    def parse(self, response):
        self.logger.warning(response.xpath(self.table_xpath_str + "/tbody/tr").extract_first("Non found!!!"))
