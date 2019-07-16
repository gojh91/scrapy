# -*- coding: utf-8 -*-
import scrapy
import re
import scrapy
from news.items import NewsItem
from datetime import timedelta, date
from urllib import parse
import time
import random
from time import sleep

start_date = date(2015, 1, 1)
end_date = date(2015, 12, 31)
cnt_per_page = 10
keyword = "금리"



url_format = "https://search.naver.com/search.naver?where=news&query={1}&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds={0}&de={0}&docid=&nso=so%3Ar%2Cp%3Afrom{0}to{0}%2Ca%3Aall&mynews=1&refresh_start=0&related=0&start={2}"


class NewsscrapySpider(scrapy.Spider):
    name = 'newsscrapy'
    
    start_urls = []
    def daterange(start_date, end_date):
        for n in range((int ((end_date - start_date).days)+1)):
            yield start_date + timedelta(n)
    for single_date in daterange(start_date, end_date):
        start_urls.append(url_format.format(single_date.strftime("%Y%m%d"), keyword, 1))
    def parse(self, response):
        for href in response.xpath("//ul[@class='type01']/li/dl/dt/a/@href").extract():
            if 'edaily.co.kr' in href:
                if 'smedaily.co.kr' not in href:
                    yield response.follow(href, self.parse_details)

            if 'news.naver.com' in href:
                yield response.follow(href, self.parse_naver)

        total_cnt = int(re.sub('[()건,]', '', response.xpath("//div[@class='title_desc all_my']/span/text()").get().split('/')[1]))
        query_str = parse.parse_qs(parse.urlsplit(response.url).query)
        currpage = int(query_str['start'][0]) 
        
        startdate = query_str['ds'][0]
        print("=================== [" + startdate + '] ' + str(currpage) + '/' + str(total_cnt) + "===================") 
        if currpage  < total_cnt : 
            yield response.follow(url_format.format(startdate, keyword, currpage+10), self.parse)

    def parse_details(self, response):    
        item = NewsItem()
        item['url'] = response.url
        item['title'] = str(response.xpath("//*[@id='contents']/section[1]/section[1]/div[1]/div[1]/h2/text()").get())
        str1 = str(response.xpath("//*[@id='contents']/section[1]/section[1]/div[1]/div[1]/div/div/ul/li[1]/p[1]/text()").get())
        item['date'] = str1.replace('등록', '').strip()
        content = str(response.xpath("//*[@id='contents']/section[1]/section[1]/div[1]/div[3]/div[1]/text()").getall())

        if item['title'] == 'None':
            item['title'] = str(response.xpath("//div[@class='dable-content-wrapper']/p/text()").get())
            str1 = str(response.xpath("//div[@class='section-content']/div/p/span/text()").get())
            item['date'] = str1.replace('등록', '').strip()
            content = str(response.xpath("//div[@class='dable-content-wrapper']/p/text()").getall())
            
        content = re.sub(' +', ' ', str(re.sub(re.compile('<.*?>'), ' ', content.replace('\\t','')).replace('\\r','').replace('\t','').replace('\\xa01','').replace('\\xa0','').replace('"','').replace("'",'').replace('\r\n','').replace('\n','').replace('\t','').replace('\u200b','').replace('\\r\\n','').replace('\\n','').strip()))
        item['content'] = content  
        if item['content'] != None:
            yield item

    def parse_naver(self, response):    
        if response.xpath('//*[@id="main_content"]/div[1]/div[1]/a/img/@title').get() == '이데일리':
            item = NewsItem()
            item['url'] = response.url
            item['title'] = str(response.xpath("//*[@id='articleTitle']/text()").get())
            str1 = str(response.xpath("//*[@id='main_content']/div[1]/div[3]/div/span/text()").get())
            item['date'] = str1.replace('등록', '').strip()
            content = str(response.xpath("//div[@id='articleBodyContents']/text()").getall())

            # if item['title'] == 'None':
            #     item['title'] = str(response.xpath("//div[@class='dable-content-wrapper']/p/text()").get())
            #     item['date'] = response.xpath("//div[@class='section-content']/div/p/span/text()").get()
            #     content = str(response.xpath("//div[@class='dable-content-wrapper']/p/text()").getall())
                
            content = re.sub(' +', ' ', str(re.sub(re.compile('<.*?>'), ' ', content.replace('\\t','')).replace('\\r','').replace('\t','').replace('\\xa01','').replace('\\xa0','').replace('"','').replace("'",'').replace('\r\n','').replace('\n','').replace('\t','').replace('\u200b','').replace(',','').replace('\\r\\n','').replace('\\n','').strip()))
            item['content'] = content  
            if item['content'] != None:
                yield item
    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url,
    #                             # cookies={'news_office_checked':'1001,1018,2227'},
    #                             cookies={'news_office_checked':'1018'},
    #                                     callback=self.parse)
    # def parse(self, response):
    #     for href in response.xpath("//ul[@class='type01']/li/dl/dt/a/@href").extract():
    #         print("#"*100)
    #         print(href)
    #         print("#"*100)
    #         self.num += 1
    #         print(self.num)
    #         yield response.follow(href, self.parse_details)

    # def parse_url(self, response):    
    #     iframe_url = response.xpath("//iframe/@src").get()
    #     if iframe_url != None :
    #         href = 'https://blog.naver.com' + response.xpath("//iframe/@src").get()
    #         yield response.follow(href, self.parse_details)

    # def parse_details(self, response):
    #     print("*"*100)
    #     item = NewsItem()
    #     item['url'] = response.url
    #     item['title'] = str(response.xpath("//*[@id='contents']/section[1]/section[1]/div[1]/div[1]/h2/text()").get())
    #     item['date'] = str(response.xpath("//*[@id='contents']/section[1]/section[1]/div[1]/div[1]/div/div/ul/li[1]/p[1]/text()").get())
    #     item['content'] = str(response.xpath("//*[@id='contents']/section[1]/section[1]/div[1]/div[3]/div[1]/text()").get())
    #     print(item['url'])
    #     print(item['title'])
    #     print(item['date'] )
    #     print(item['content'])
    #     yield {
    #         'url' : response.url
    #     }
