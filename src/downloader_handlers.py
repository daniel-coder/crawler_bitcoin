# -*-coding:utf-8-*-

# from scrapy.core.downloader import Downloader
# from scrapy.core.downloader.handlers.file import FileDownloadHandler
# from scrapy.core.downloader.handlers.http import HttpDownloadHandler
# from scrapy.core.downloader.handlers.http import HttpDownloadHandler
# from scrapy.core.downloader.handlers.s3 import S3DownloadHandler

from copy import deepcopy
from platform import system as get_os
from urllib.parse import urlparse, urlunparse

from scrapy import twisted_version
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import PhantomJS, Chrome, ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait

if twisted_version >= (11, 1, 0):
    from scrapy.core.downloader.handlers.http11 import HTTP11DownloadHandler as HTTPDownloadHandler
else:
    from scrapy.core.downloader.handlers.http10 import HTTP10DownloadHandler as HTTPDownloadHandler


class JsHandler(object):
    def __init__(self, settings):
        self.check_wait_time = settings.get("WEBDRIVER_CHECK_WAIT_TIME", 0.1)
        self.page_load_timeout = settings.get('WEBDRIVER_LOAD_TIMEOUT', 60)

    def wait_xpath(self, driver, xpath):
        wait = WebDriverWait(driver, 30, poll_frequency=self.check_wait_time)
        try:
            wait.until(lambda dr: dr.find_element_by_xpath(xpath))
        except TimeoutException:
            pass

    def get_driver(self, request):
        raise NotImplementedError

    def download_request(self, request, spider):
        meta = request.meta
        js_finish_xpath = meta.get("JS_Finish_Xpath", None)
        url = meta.get("Original_Url", urlunparse(("http",) + urlparse(request.url)[1:]))

        driver = self.get_driver(request)
        try:
            # TODO 处理cookie
            driver.get(url)

            if js_finish_xpath:  # 等待元素加载
                self.wait_xpath(driver, js_finish_xpath)

            html_body = driver.page_source
            headers = request.headers
            return HtmlResponse(url, encoding="utf-8", body=html_body,
                                headers=headers, request=request)
        except Exception:
            raise
        finally:
            driver.close()


class PhantomJSHandler(JsHandler):
    def __init__(self, settings):
        super().__init__(settings)
        self.executable_path = settings['PHANTOMJS_EXECUTABLE_PATH']
        self.service_args = settings.get('PHANTOMJS_OPTIONS', ["--load-images=false",
                                                               "--disk-cache=false"])
        self.dcap = DesiredCapabilities.PHANTOMJS.copy()
        self.dcap["phantomjs.page.settings.resourceTimeout"] = self.page_load_timeout * 1000  # 单位是毫秒

    def get_driver(self, request):
        proxy = request.meta.get("proxy", None)
        if not proxy:
            service_args = self.service_args
        else:
            service_args = self.service_args.copy()
            p = urlparse(proxy)
            service_args += ["--proxy=" + (p.netloc or p.path),
                             "--proxy-type=" + (p.scheme or "http")]

        ua = request.headers.get('User-Agent',
                                 b'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/59.0')
        self.dcap["phantomjs.page.settings.userAgent"] = ua.decode()

        driver = PhantomJS(executable_path=self.executable_path,
                           service_args=service_args,
                           desired_capabilities=self.dcap)
        driver.set_page_load_timeout(self.page_load_timeout)
        driver.set_script_timeout(self.page_load_timeout)
        return driver


class HeadlessChromeHandler(JsHandler):
    def __init__(self, settings):
        super().__init__(settings)
        self.executable_path = settings['CHROME_EXECUTABLE_PATH']
        self.dcap = DesiredCapabilities.CHROME.copy()
        options = ChromeOptions()
        if 'Windows' == get_os():
            options.binary_location = settings["HEADLESS_CHROME_PATH"]
        options.add_argument('no-sandbox')
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        if not settings.get("CHROME_LOAD_IMAGES", False):
            options.add_argument('disable-images')
        self.options = options

    def get_driver(self, request):
        proxy = request.meta.get("proxy", None)
        if not proxy:
            options = self.options
        else:
            options = deepcopy(self.options)
            options.add_argument('--proxy-server=' + proxy)

        return Chrome(executable_path=self.executable_path,
                      desired_capabilities=self.dcap,
                      chrome_options=options)
