# _*_ coding: utf-8 _*_

import urllib2
import itertools
import datetime
import time# 连接爬虫
import urlparse
import re
import robotparser


# 设置同一域名下载的访问间隔
class Throttle:
    """Add a delay between download to the same domain
    eg:
    throttle = Throttle(5)
    ...
    throttle.wait(url)
    result = download(url, headers, proxy=..., num_retries=2)
    """
    def __init__(self, delay):
        # 每次下载操作之间的停顿间隔
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        # 得到当前网址的域名. 并将这个域名作为Key, 当前时间作为value, 存储到字典中
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed) .seconds
            if sleep_secs > 0:
                # domain has been accessed recently
                # so need to sleep
                time.sleep(sleep_secs)
        # update the last accessed time
        self.domains[domain] = datetime.datetime.now()


# 设定下载的接口
def download(url, user_agent='wswp', proxy=None, num_retries=2):
    print 'Downloading: ', url
    headers = {'user_agent': user_agent }
    request = urllib2.Request(url, headers=headers)

    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html = opener.open(request).read()
    except urllib2.URLError as e:
        print 'Download error: ', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, user_agent, num_retries-1)
    return html
# 下面是一个遍历ID的爬虫,并且当ID不连续的时候会在一定次数内自动重连接
# 重新下载下一ID的HTML的最大次数
max_errors = 5
# 当前已经下载的次数
num_errors = 0
# 爬取ID递增的HTML, 并且允许跳过重复
for page in itertools.count(1):
    url = 'http://example/webscraping.com/view/-%d' % page
    html = download(url)
    if html is None:
        num_errors += 1
        if num_errors == max_errors:
            # 只有当 None 的次数达到5才会退出循环
            break
    else:
        num_errors = 0


# 下面是一个能爬取一个域名内所有制定网站的爬虫
def link_crawler(seed_url, link_regex, robots=False):
    """爬取seed link和那些匹配regex的link"""
    crawl_queue = [seed_url]
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        # 检查url是否通过了robots.txt
        if robots == True:
            rp = robotparser.RobotFileParser()
            rp.set_url(urlparse.urljoin(seed_url, '/robots.txt'))
            user_agent = 'wswp'
            if not rp.can_fetch(user_agent , url):
                print 'Forbidden by robots.txt'
                continue
        html = download(url)
        # 将匹配正则表达式的link筛选出来
        for link in get_links(html):
            # 将相对路径转换成绝对路径
            regex = re.compile('^http')
            # 判断是否为绝对路径
            if not re.match(regex, html):
                if re.match(link_regex, link):
                    link = urlparse.urljoin(seed_url, link)
            if link not in seen:
                seen.add(link)
                crawl_queue.append(link)


def get_links(html):
    """返回html内的links的列表"""
    # 首先需要一个正则表达式把给定html内的链接标签的内容抽取出来
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    # 生成列表
    return webpage_regex.findall(html)
