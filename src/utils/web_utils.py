from random import choice as rand_choice
from time import time

from requests import get as http_get, post as http_post
from urllib.request import urlopen, Request

ASK_TIMEOUT = 61  # web访问超时时间

# http://www.useragentstring.com/pages/useragentstring.php
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2251.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36 QIHU 360SE',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3) QQBrowser/6.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36 TheWorld 6',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3647.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 BIDUBrowser/7.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 LBBROWSER',
]


def get_one_ua():
    return rand_choice(USER_AGENT_LIST)


def get_js_time():
    return str(int(time() * 1E3))


def find_str_range(str_obj, start_str, end_str):
    """
    截取字符串
    """
    start_index = str_obj.find(start_str)
    if start_index >= 0:
        return str_obj[start_index:str_obj.find(end_str, start_index)]
    elif isinstance(start_str, str):
        return ""
    else:
        return b""


def get_response_by_requests(url, headers, cookie_str=None, cookie_jar=None, proxies=None):
    if cookie_str is not None:
        headers['Cookie'] = cookie_str

    kwargs = {"headers": headers,
              "timeout": ASK_TIMEOUT,
              "verify": False,
              "proxies": proxies,
              }

    if cookie_jar is not None:
        kwargs["cookies"] = cookie_jar

    return http_get(url, **kwargs)


def get_content_by_requests(url, headers, cookie_str=None, cookie_jar=None, proxies=None):
    resp = get_response_by_requests(url, headers=headers,
                                    cookie_str=cookie_str, cookie_jar=cookie_jar, proxies=proxies)
    return resp.content


def get_response_by_requests_post(url, headers, data=None, json=None,
                                  cookie_str=None, cookie_jar=None, proxies=None):
    if cookie_str is not None:
        headers['Cookie'] = cookie_str

    kwargs = {"headers": headers,
              "timeout": ASK_TIMEOUT,
              "verify": False,
              "proxies": proxies,
              }

    if cookie_jar is not None:
        kwargs["cookies"] = cookie_jar

    return http_post(url, data=data, json=json, **kwargs)


def get_content_by_requests_post(url, headers, data=None, json=None,
                                 cookie_str=None, cookie_jar=None, proxies=None):
    resp = get_response_by_requests_post(url, headers=headers, data=data, json=json,
                                         cookie_str=cookie_str, cookie_jar=cookie_jar, proxies=proxies)
    return resp.content


def get_headers_from_response(response):
    return {k: (v[0] if v else "") for k, v in response.request.headers.items()}


def get_cookie_header_by_urlopen(url):
    req_header = {'User-Agent': get_one_ua(),
                  'Accept-Language': 'zh-CN,zh',
                  'Connection': 'close',
                  }
    req = Request(url, None, req_header)
    resp = urlopen(req, None, ASK_TIMEOUT)
    cookie = "".join(resp.headers.get_all("set-cookie"))
    resp.close()
    return cookie
