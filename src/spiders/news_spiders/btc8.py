# -*- coding: utf-8 -*-

from dateutil.parser import parse
from scrapy import Request

from src.items.news_items import NewsItem
from src.spiders.spider_classes import NoticeChangeSpider, NoticeClosedSpider


class Btc8Spider(NoticeChangeSpider, NoticeClosedSpider):
    name = "8btc"
    allowed_domains = ["8btc.com"]
    start_urls = ["http://www.8btc.com/cypherpunk"]

    custom_settings = {
        'DOWNLOAD_DELAY': 100,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    }

    def parse(self, response):
        sel_list = response.xpath("//div[@id='list']/article")
        if not sel_list:
            self.notice_change("No data found!!!!! " + response.url)

        for sel in sel_list:
            # title = sel.xpath(".//div[contains(@class,'article-title')]/a/@title").extract_first("")
            # time = sel.xpath(".//div[contains(@class,'article-info')]/span/text()").extract_first("")
            url = sel.xpath(".//div[contains(@class,'flipInY')]//a/@href").extract_first("")
            yield Request(url, self.parse_news)

        url = response.xpath("//div[@id='zan-page']//a[text()='»']/@href").extract_first()
        if url:
            yield Request(url, self.parse, dont_filter=True)
        else:  # 没有下一页时，重头从第一页开始
            yield Request(self.start_urls[0], self.parse, dont_filter=True)

    def parse_news(self, response):
        main_div = response.xpath("//div[@id='zan-bodyer']")
        item = NewsItem()
        item["title"] = main_div.xpath(".//div[@class='article-title']/h1/text()").extract_first("")
        item["read_count"] = int(main_div.xpath(".//div[@class='single-crumbs clearfix']/span[@class='pull-right fa-eye-span']/i/following::text()").extract_first("").strip())
        item["pic"] = main_div.xpath(".//img/@src").extract_first("")
        item["time"] = parse(main_div.xpath(".//time/@datetime").extract_first(""))
        item["content"] = main_div.xpath(".//div[@class='article-content']").extract_first("")
        item["url"] = response.url
        yield item
