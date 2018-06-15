# -*- coding: utf-8 -*-

from src.data_storage.db_settings import MYSQL_BITMESSAGES_TABLE
from src.items.message_item import MessageItem
from src.pipelines.base import MysqlPipelineUtils


class MessagePipeline(MysqlPipelineUtils):
    def __init__(self):
        super().__init__(MessageItem, MYSQL_BITMESSAGES_TABLE)

    def write_item_to_db(self, item):
        cursor = self.mysql_conn.cursor()
        cursor.execute("SELECT time FROM " + MYSQL_BITMESSAGES_TABLE + " WHERE url=%s", item["url"])
        if not cursor.fetchone():
            base_sql = "INSERT INTO " + MYSQL_BITMESSAGES_TABLE + " ("
            agrs = []
            for name, value in item.items():
                base_sql += name + ","
                agrs.append(value)
            base_sql = base_sql.rstrip(",") + ") VALUES (" + ("%s," * len(agrs))
            cursor.execute(base_sql.rstrip(",") + ")", agrs)
