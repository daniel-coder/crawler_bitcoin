from pprint import pformat
from time import sleep
from urllib.parse import urlsplit

from scrapy import Spider, Request
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.utils.project import get_project_settings
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome, PhantomJS, ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.web_utils import get_one_ua


class ErrCallbackSpider(Spider):
    def log_err_callback(self, failure):
        log_msg = ("url: %s" % failure.request.url)
        if failure.check(HttpError):
            log_msg += " status: %s" % failure.value.response.status

        log_msg += "\n" + repr(failure)
        self.logger.warning(log_msg)

    def retry_again_err_callback(self, failure):
        self.log_err_callback(failure)
        return failure.request.copy()

    def retry_twice_err_callback(self, failure):
        self.log_err_callback(failure)

        try:
            request = failure.request
            meta = request.meta
            retry_count = meta.setdefault("err_callback_retry", 0)
            if retry_count < 2:
                new_request = request.copy()
                new_request.meta["err_callback_retry"] += 1
                self.logger.warning("当前请求url: {0} 重试次数: {1}".format(request.url, retry_count + 1))
                sleep(1)
                return new_request
            else:
                if "item" in meta:
                    return meta["item"]
        except Exception:
            self.logger.exception("err_callback except")


class LoggingClosedSpider(Spider):
    """
    爬虫关闭时记录日志
    """

    def closed(self, reason):
        myname = myaddr = ""
        try:
            import socket
            myname = socket.getfqdn(socket.gethostname())  # 获取本机电脑名
            myaddr = socket.gethostbyname(myname)  # 获取本机ip
        except Exception:
            pass

        stats = self.crawler.stats.get_stats()
        stats["spended_time"] = str(stats["finish_time"] - stats["start_time"])
        msg = "Spider[%s] @%s(%s) closed with reason: [%s]\n%s" \
              % (self.name, myaddr, myname, reason, pformat(stats))
        self.logger.critical(msg)
        return msg


class NoticeClosedSpider(LoggingClosedSpider):
    """
    爬虫关闭时发送邮件通知
    """

    def closed(self, reason):
        msg = super().closed(reason)


class NoticeChangeSpider(Spider):
    """
    提供一个函数，在页面变化时发送邮件通知
    """

    def notice_change(self, msg):
        self.logger.critical(msg)


class WebdriverSpider(Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = get_project_settings()
        self.check_wait_time = settings.get("WEBDRIVER_CHECK_WAIT_TIME", 0.1)
        self.page_load_timeout = settings['WEBDRIVER_LOAD_TIMEOUT']
        self.dcap = {}

    def wait_xpath(self, driver, xpath, raise_timeout=False, timeout=30, displayed=False):
        wait = WebDriverWait(driver, timeout, poll_frequency=self.check_wait_time)
        try:
            wait.until(lambda dr: dr.find_element_by_xpath(xpath))
            if displayed:
                wait.until(lambda dr: dr.find_element_by_xpath(xpath).is_displayed())
        except TimeoutException:
            if not raise_timeout:
                pass
            else:
                raise

    def get_driver(self):
        raise NotImplementedError

    def load_page_by_webdriver(self, url, finish_xpath=None):
        # TODO 处理代理
        driver = self.get_driver()
        driver.set_page_load_timeout(self.page_load_timeout)
        driver.set_script_timeout(self.page_load_timeout)
        for i in range(2):
            try:
                driver.get(url)
                if finish_xpath:
                    self.wait_xpath(driver, finish_xpath)
            except Exception:
                self.logger.exception("")
                continue
            else:
                break

        return driver


class PhantomJSWebdriverSpider(WebdriverSpider):
    """
    提供一个函数，返回Phantomjs执行页面请求的webdriver
    """

    def __init__(self, *args, load_images=False, **kwargs):
        super().__init__(*args, **kwargs)
        settings = get_project_settings()
        self.executable_path = settings['PHANTOMJS_EXECUTABLE_PATH']
        self.service_args = ["--load-images=" + str(load_images).lower(),
                             "--disk-cache=false"]
        self.dcap = DesiredCapabilities.PHANTOMJS.copy()
        self.dcap["phantomjs.page.settings.resourceTimeout"] = self.page_load_timeout * 1000  # 单位是毫秒

    def get_driver(self):
        self.dcap["phantomjs.page.settings.userAgent"] = get_one_ua()
        return PhantomJS(executable_path=self.executable_path,
                         service_args=self.service_args,
                         desired_capabilities=self.dcap)


class ChromeWebdriverSpider(WebdriverSpider):
    """
    提供一个函数，返回Chrome执行页面请求的webdriver
    """

    def __init__(self, *args, load_images=True, **kwargs):
        super().__init__(*args, **kwargs)
        settings = get_project_settings()

        self.executable_path = settings['CHROME_EXECUTABLE_PATH']
        self.dcap = DesiredCapabilities.CHROME.copy()

        options = ChromeOptions()
        if not load_images:
            options.add_argument('disable-images')
        self.options = options

    def get_driver(self):
        return Chrome(executable_path=self.executable_path,
                      desired_capabilities=self.dcap,
                      chrome_options=self.options)


class HeadlessChromeWebdriverSpider(ChromeWebdriverSpider):
    """
    提供一个函数，返回Headless Chrome执行页面请求的webdriver
    """

    def __init__(self, *args, load_images=False, **kwargs):
        super().__init__(*args, load_images=load_images, **kwargs)
        options = self.options
        options.add_argument('no-sandbox')
        options.add_argument('headless')
        options.add_argument('disable-gpu')


class JsRequestSpider(Spider):
    """
    使用无头浏览器自动加载每一个页面请求
    """

    def __init__(self, *args, js_finish_xpath=None, **kwargs):
        """
        :param js_finish_xpath: 判断页面是否加载完成的xpath
        """
        super().__init__(*args, **kwargs)
        self.js_finish_xpath = js_finish_xpath
