#!/usr/bin/env python
# -*-coding:utf-8 -*-
import requests
import lxml.html
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Downloader:
    def __init__(self, url, scrape_callback=None):
        self.url = url
        self.scrape_callback = scrape_callback

    def get_download_url(self):
        # '''获取每个电影详情页的url'''
        url_list =[]
        # for i in range(1,22803):
        for i in range(1):
            url = self.url+'?offset='+str(30*i)
            response = requests.get(url)
            if response.status_code == 200:
                html = response.text
                tree = lxml.html.fromstring(html)
                # 使用xpath方式获取div下的所有a标签
                ll = tree.xpath(u"//div/a")
                # 遍历ll
                for i in ll:
                    # 获取a标签的href信息
                    url_str = i.get('href')
                    # 判断url_str
                    if url_str is not None:
                        # 判断url_str是否有'films'中,有的话则是我们要找的内容
                        if re.search('films', url_str) is not None:
                            # 判断，不保存重复的url
                            if i.get('href') not in url_list:
                                url_list.append(i.get('href'))

        return url_list

    def download(self):
        # ''''抓取url信息中的电影名称，等信息'''
        # 获取所有详情页的url
        url_list = self.get_download_url()
        for url_num in url_list:
            # 查看元素可知返回的是‘films/2333’只需把后缀的/和数字填入到默认url中就是具体详情页
            urlpage = self.url+'/'+str(url_num).split('/')[-1]
            # url请求
            response = requests.get(urlpage)
            # 判断，如果能正常相应则继续
            if response.status_code == 200:
                html = response.text
                # 规范html
                tree = lxml.html.fromstring(html)
                # 判断scrape_callback，True则保存信息
                if self.scrape_callback:
                    # 通过CSS选择器获取想要的内容
                    l_img = tree.cssselect('div.avater-shadow > img.avater')[0].get('src')
                    l_filmname = tree.cssselect('div.movie-brief-container > h3.name')[0].text_content()
                    l_type = tree.cssselect('div.movie-brief-container > ul> li.ellipsis')[0].text_content()
                    l_director = tree.cssselect('div.info > a.name')[0].text_content()
                    row = [l_filmname, l_director, l_type, l_img]
                    self.scrape_callback(row)


if __name__ == '__main__':
    url = 'http://maoyan.com/films'
    d = Downloader(url)
    d.download()
