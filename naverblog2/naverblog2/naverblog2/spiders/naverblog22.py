# -*- coding: utf-8 -*-
import scrapy


class Naverblog22Spider(scrapy.Spider):
    name = 'naverblog22'
    allowed_domains = ['naver.com']
    start_urls = ['http://naver.com/']

    def parse(self, response):
        pass
