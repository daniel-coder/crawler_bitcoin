# -*- coding: utf-8 -*-

from re import compile as re_compile
from dateutil.parser import parse
from scrapy import Request, FormRequest

from src.items.news_items import NewsItem
from src.spiders.spider_classes import NoticeChangeSpider, NoticeClosedSpider


class BitkanSpider(NoticeChangeSpider, NoticeClosedSpider):
    name = "bitkan"
    allowed_domains = ["bitkan.com"]
    start_urls = ["http://bitkan.com/news"]

    custom_settings = {
        'DOWNLOAD_DELAY': 100,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    }

    PAGE_PATTEN = re_compile(r"getData\((\d+)\)")

    def parse(self, response):
        sel_list = response.xpath("//div[contains(@class,'news-v3-in-sm')]"
                                  "//h4[@class='news-title']/a/@href")
        if not sel_list:
            self.notice_change("No data found!!!!! " + response.url)

        for url in sel_list.extract():
            yield Request(url, self.parse_news)

        onclick = response.xpath("//ul[@class='pagination']//a[text()='>>']/@onclick").extract_first()
        if onclick:
            page = self.PAGE_PATTEN.search(onclick).group(1)
            url = "http://bitkan.com/news/load_news/" + page
            yield FormRequest(url, self.parse, formdata={"page": page}, dont_filter=True)
        else:  # 没有下一页时，重头从第一页开始
            yield Request(self.start_urls[0], self.parse, dont_filter=True)

    def parse_news(self, response):
        main_div = response.xpath("//div[@class='news-v3-in']")
        item = NewsItem()
        item["title"] = main_div.xpath(".//h2/text()").extract_first("")
        item["pic"] = main_div.xpath(".//img/@src").extract_first("")
        item["time"] = parse(main_div.xpath(".//li[last()]/text()").extract_first(""))
        item["content"] = main_div.xpath(".//div[last()]").extract_first("")
        item["url"] = response.url
        yield item
