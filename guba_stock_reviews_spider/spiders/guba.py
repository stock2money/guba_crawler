# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from guba_stock_reviews_spider.items import GubaReviewItem

class GubaSpider(scrapy.Spider):
    name = 'guba'
    allowed_domains = ['guba.com', 'guba.eastmoney.com']
    start_urls = []
    base_url = 'http://guba.eastmoney.com/default,0_%d.html'
    root_url = 'http://guba.eastmoney.com'
    stocks = {}
    pages = 200

    def __init__(self):
        info = pd.read_csv("data/stocks.csv", header=0, delimiter=",")
        for i in range(len(info["display_name"])):
            self.stocks[info["display_name"][i]] = info["code"][i]
        for i in range(self.pages):
            self.start_urls.append(self.base_url % i)
    
    def parse(self, response):
        reviews = response.xpath('//*[@id="main-body"]/div[4]/div[1]/div[3]/div/div[2]/div[1]/ul/li')
        # print(reviews)
        for each in reviews:
            item = GubaReviewItem()
            name = each.xpath('./span/a[1]/text()').extract()[0][:-1]
            if name in self.stocks.keys():
                item["infoType"] = '1'
                item["code"] = self.stocks[name]
            else:
                item["infoType"] = '0'
            
            url = self.root_url + each.xpath('./span/a[2]/@href').extract()[0]
            item["href"] = url
            item["author"] = each.xpath('./cite[3]/a/text()').extract()[0]
            item["title"] = each.xpath('./span/a[2]/text()').extract()[0]
            request = scrapy.Request(url=item["href"], callback=self.parseHref)
            request.meta['item'] = item
            yield request

    def parseHref(self, response):
        item = response.meta['item']
        # print(item)
        time = response.xpath('//*[@id="zwconttb"]/div[2]/text()').extract()[0]
        item["time"] = self.getTime(time)
        
        # //*[@id="zwconbody"]/div/div/p
        # //*[@id="zw_body"]/p
        # //*[@id="zwconbody"]/div/text()

        detail = ""
        if len(response.xpath('//*[@id="zw_body"]/p')) > 0:
            article = response.xpath('//*[@id="zw_body"]/p')
            print(article)
            for p in article:
                if len(p.xpath('./text()').extract()) > 0:
                    detail += p.xpath('./text()').extract()[0]
        elif len(response.xpath('//*[@id="zwconbody"]/div/div/p')) > 0:
            article = response.xpath('//*[@id="zwconbody"]/div/div/p')
            print(article)
            for p in article:
                if len(p.xpath('./text()').extract()) > 0:
                    detail += p.xpath('./text()').extract()[0]
        else:
            detail = response.xpath('//*[@id="zwconbody"]/div/text()').extract()[0]
        item["detail"] = detail.strip()
        yield item

    def getTime(self, s):
        print(s)
        i, j = 0, len(s) - 1
        while i < len(s) - 1:
            if s[i] >= '0' and s[i] <= '9':
                break
            i += 1
        while j >= 0:
            if s[j] >= '0' and s[j] <= '9':
                break
            j -= 1
        return s[i:j+1]
