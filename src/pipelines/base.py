# -*- coding: utf-8 -*-

from hashlib import md5
from os import path as os_path

from scrapy.exceptions import DropItem
from scrapy.logformatter import LogFormatter, DROPPEDMSG, logging
from pymysql.err import Error
from src.data_storage.mysql_db import get_db_conn



class DroppedInfoLogFormatter(LogFormatter):
    def dropped(self, item, exception, response, spider):
        return {
            'level': logging.INFO,
            'msg': DROPPEDMSG,
            'args': {
                'exception': exception,
                'item': item,
            }
        }


class MysqlPipelineUtils(object):
    def __init__(self, item_class, table_name):
        self.item_class = item_class
        self.table_name = table_name

    def open_spider(self, spider):
        self.mysql_conn = get_db_conn()

    def close_spider(self, spider):
        try:
            self.mysql_conn.close()
        except Error:
            spider.logger.warning("Already closed")

    def write_item_to_db(self, item):
        raise NotImplementedError

    def process_item(self, item, spider):
        item_class = self.item_class
        if type(item) is item_class:
            try:
                self.write_item_to_db(item)
            except Exception:
                spider.logger.exception("%s write item(%s) to db error: " % (spider.name, item))
            raise DropItem("Processing %s item done." % item_class.__name__)
        else:
            return item
