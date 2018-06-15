# -*- coding: utf-8 -*-

# Scrapy settings for src project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from os import path as os_path, makedirs
from platform import system as get_os

import urllib3

from src import config

urllib3.disable_warnings()

this_dir = os_path.dirname(os_path.abspath(__file__))

BOT_NAME = 'src'

SPIDER_MODULES = ['src.spiders']
NEWSPIDER_MODULE = 'src.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/59.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.3  # 下载器在下载同一个网站下一个页面前需要等待的时间(单位:秒)
DOWNLOAD_TIMEOUT = 61  # 下载器超时时间(单位:秒)
DOWNLOAD_MAXSIZE = 67108864  # 64M

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
# CONCURRENT_REQUESTS_PER_IP = 0

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False
COOKIES_DEBUG = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'src.middlewares.SrcSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'src.downloader_middlewares.RandomUserAgentDownloaderMiddleware': 1,
    'src.downloader_middlewares.JsDownloaderMiddleware': 2,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 3,
}

DOWNLOAD_HANDLERS = {
    'js': 'src.downloader_handlers.PhantomJSHandler',  # 需要执行js动态生成页面的情况
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'src.pipelines.news_pipelines.NewsPipeline': 100,
    'src.pipelines.message_pipelines.MessagePipeline': 101,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

LOG_FORMATTER = 'src.pipelines.base.DroppedInfoLogFormatter'

if 'Windows' == get_os():  # 开发人员调试环境
    LOG_FILE = None
    LOG_LEVEL = "WARNING"

    PHANTOMJS_EXECUTABLE_PATH = os_path.join(this_dir, 'browsers', 'phantomJS', 'phantomjs.exe')
    CHROME_EXECUTABLE_PATH = os_path.join(this_dir, 'browsers', 'chrome', 'chromedriver.exe')

else:  # Linux生产环境
    LOG_FILE = config.SCRAPY_LOG_FILE
    LOG_LEVEL = config.SCRAPY_LOG_LEVEL

    PHANTOMJS_EXECUTABLE_PATH = os_path.join(this_dir, 'browsers', 'phantomJS', 'phantomjs')
    CHROME_EXECUTABLE_PATH = os_path.join(this_dir, 'browsers', 'chrome', 'chromedriver')


PHANTOMJS_OPTIONS = ['--load-images=false',
                     '--disk-cache=false'
                     ]
CHROME_LOAD_IMAGES = False
WEBDRIVER_CHECK_WAIT_TIME = 0.1
WEBDRIVER_LOAD_TIMEOUT = 60  # 页面加载超时，单位秒
