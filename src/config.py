# -*- coding: utf-8 -*-

from os import path as os_path

this_dir = os_path.dirname(os_path.abspath(__file__))

# SCRAPY的配置：src -> settings.py
SCRAPY_LOG_FILE = os_path.join(this_dir, "log", "crawler.log")
SCRAPY_LOG_LEVEL = "ERROR"


# 数据库地址配置：data_storage -> db_settings
DATA_STORAGE_MYSQL_SETTINGS = {
    'local': {
        'db': 'test',
        'user': 'root',
        'passwd': '123456',
        'host': '39.105.128.88',
        'port': 3306,
        # 'unix_socket': "MySQL",
        # 'named_pipe': True,
    },
}
