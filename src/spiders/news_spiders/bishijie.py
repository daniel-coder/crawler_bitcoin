# -*- coding: utf-8 -*-

from dateutil.parser import parse
from scrapy import Request
import sys
import time

from src.items.message_item import MessageItem
from src.spiders.spider_classes import NoticeChangeSpider


class BishijieSpider(NoticeChangeSpider):
    name = "bishijie"
    allowed_domains = ["bishijie.com"]
    start_urls = ["https://www.bishijie.com/kuaixun"]

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    }

    # def start_requests(self):
    #     while True:
    #         yield
    #         time.sleep(30)

    def parse(self, response):
        live_list = response.xpath("//div[contains(@class,'live livetop')]")
        if not live_list:
            self.notice_change("No data found!!!!! " + response.url)

        for live in live_list:
            # title = sel.xpath(".//div[contains(@class,'article-title')]/a/@title").extract_first("")
            # time = sel.xpath(".//div[contains(@class,'article-info')]/span/text()").extract_first("")
            ul_list = live.xpath(".//ul")
            for ul in ul_list:
                item = MessageItem()
                item["time"] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(ul.xpath('./@id').extract_first(""))))
                item["url"] = ul.xpath(".//li[@class='lh32 orange']/div/a/@href").extract_first("")
                item["title"] = ul.xpath(".//li[@class='lh32 orange']/div/a/@title").extract_first("")
                item["content"] = ul.xpath(".//li[@class='lh32 orange']/div/a/text()").extract_first("")
                item["up"] = ul.xpath(".//li[@class='vote']/div[@class='seemore  left']/b/text()").extract_first("")
                item["down"] = ul.xpath(".//li[@class='vote']/div[@class='bearish  left']/b/text()").extract_first("")
                yield item


