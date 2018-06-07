# -*- coding: utf-8 -*-

from src.data_storage.db_settings import MYSQL_BITNEWS_TABLE
from src.items.news_items import NewsItem
from src.pipelines.base import MysqlPipelineUtils


class NewsPipeline(MysqlPipelineUtils):
    def __init__(self):
        super().__init__(NewsItem, MYSQL_BITNEWS_TABLE)

    def write_item_to_db(self, item):
        cursor = self.mysql_conn.cursor()
        cursor.execute("SELECT time FROM " + MYSQL_BITNEWS_TABLE + " WHERE url=%s", item["url"])
        if not cursor.fetchone():
            base_sql = "INSERT INTO " + MYSQL_BITNEWS_TABLE + " ("
            agrs = []
            for name, value in item.items():
                base_sql += name + ","
                agrs.append(value)
            base_sql = base_sql.rstrip(",") + ") VALUES (" + ("%s," * len(agrs))
            cursor.execute(base_sql.rstrip(",") + ")", agrs)
