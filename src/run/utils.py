# -*- coding: utf-8 -*-

from collections import Iterable
from multiprocessing import Process
from time import sleep

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def run_scrapy_spider(spider_or_spiderList):
    process = CrawlerProcess(get_project_settings())

    if not isinstance(spider_or_spiderList, Iterable):
        spider_list = [spider_or_spiderList]
    else:
        spider_list = spider_or_spiderList

    for spider in spider_list:
        process.crawl(spider)

    process.start()


def run_multiple_spider_with_process(spider_dict, process_count=1):
    process_dict = {}
    for name, spider in spider_dict.items():
        for i in range(process_count):
            p = Process(target=run_scrapy_spider, args=(spider,))
            p.start()
            process_dict[name + "_" + str(i)] = p
            sleep(1)

    for name, process in process_dict.items():
        process.join()


def run_spider_forever_by_process(spider, interval=61):
    while True:
        p = Process(target=run_scrapy_spider, args=(spider,))
        p.start()
        p.join()
        del p

        sleep(interval)
