# _*_ coding: utf-8 _*_
# __author__ = 'syss'
# __date__ = '2017/5/23 0023 下午 4:28'
import random
import pickle
import os
from final_crawler import Throttle
import re
import urlparse
import urllib2


max_length = 500


# 将download函数设定成类, 并为它添加新的功能
class Downloader:
    def __init__(self, delay=5, user_agent='wswp', proxies=None, num_retries=1, cache=None):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache

    # 检查是否已经存在缓存, 如果没有存在缓存就调用下载的方法
    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                # 表明没有相关的缓存
                pass
            # 查看状态码, 如果是服务器错误说明缓存是无效的, 故清除缓存并重新下载
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    # 服务器错误, 无视缓存的结果并重新下载
                    result = None
        if result is None:
            # 说明没有缓存
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy, self.num_retries - 1)
            if self.cache:
                # 保存结果到缓存
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, num_retries, data=None):
        print 'Downloading', url
        request = urllib2.Request(url, data, headers or {})
        opener = urllib2.build_opener()
        code = None
        if proxy:
            proxy_params = {urlparse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_params))
        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
        except urllib2.URLError as e:
            print 'Download error: ', e.reason
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code < 600:
                    # 5XX服务器错误, 重新尝试下载
                    return self.download(url, headers, proxy, num_retries - 1, data)
                else:
                    code = None
        return {'html': html, 'code': code}


# 定义cache类
class DiskCache:
    def __init__(self, cache_dir='cache'):
        self.cache_dir = cache_dir
        self.max_length = max_length

    def url_to_path(self, url):
        """Create file system path for this URL
        """
        components = urlparse.urlsplit(url)
        # 将 index.html 添加到空的path中
        '''
        通过将末尾的'/'去掉, 防止出现'XXX/XXX//index.html'这样的情况...
        也可以使用os.path.join等方法
        '''
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query
        # 将 filename 中的非法字符进一步替换
        filename = re.sub('[^/0-9a-zA-Z\-.,;_ ]', '_', filename)
        # 将目录及其子目录的长度限定在255个字符以内
        filename = '/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir, filename)

    def __getitem__(self, url):
        """从硬盘中读取这个URL的数据"""
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                return pickle.load(fp)
        else:
            # 这个URL还没被缓存
            raise KeyError(url + 'does not exist')

    def __setitem__(self, url, result):
        """将这个url的数据保存到硬盘中"""
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(path, 'wb') as fp:
            fp.write(result)
