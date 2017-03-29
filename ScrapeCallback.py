#!/usr/bin/env python
# -*-coding:utf-8 -*-
import csv
import downloader
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class ScrapeCallback:
    '''下载的信息保存到csv中'''
    def __init__(self):
        fileobj=open("maoyan.csv", 'w')
        self.writer = csv.writer(fileobj)
        self.films = ('film_name', 'director', 'film_type', 'film_cover')
        self.writer.writerow(self.films)

    def __call__(self, row):
        self.writer.writerow(row)

if __name__ == '__main__':
    url = 'http://maoyan.com/films'
    d = downloader.Downloader(url, scrape_callback=ScrapeCallback())
    d.download()
