import scrapy
import time
import csv

from newscrawling.items import NewscrawlingItem


class NewsUrlSpider(scrapy.Spider):
    name = "newsUrlCrawler"

    def start_requests(self):
        print("start_requests")

        press = [8, 190, 200]  # 8: 중앙
        pageNum = 2
        date = [20180501]

        # http://media.daum.net/cp/8?page=1&regDate=20170501&cateId=1002
        for cp in press:
            for day in date:
                for i in range(1, pageNum, 1):
                    url = "http://media.daum.net/cp/{0}?page={1}&regDate={2}&cateId=1002".format(
                        cp, i, day
                    )

                    print(url)
                    time.sleep(1)
                    yield scrapy.Request(url, self.parse_news, errback=self.errback)

    def errback(self, res):
        print(res)

    def parse_news(self, response):
        print("parse_news")

        # for sel in response.xpath('//*[@id="mArticle"]/div[2]/ul/li[1]/div'
        # print(response.text)
        # xpath = response.xpath('//*[@id="mArticle"]')
        # print(xpath)

        for sel in response.xpath('//*[@id="mArticle"]/div[2]/ul/li/div'):
            print(sel)

            item = NewscrawlingItem()

            item["source"] = sel.xpath(
                'strong/span[@class="info_news"]/text()'
            ).extract()[0]
            item["category"] = "정치"
            item["title"] = sel.xpath('strong[@class="tit_thumb"]/a/text()').extract()[
                0
            ]
            item["url"] = sel.xpath('strong[@class="tit_thumb"]/a/@href').extract()[0]
            item["date"] = sel.xpath(
                'strong[@class="tit_thumb"]/span/span[@class="info_time"]/text()'
            ).extract()[0]

            print("*" * 100)
            print(item["title"])

            yield item


class NewsSpider(scrapy.Spider):
    name = "newsCrawler"

    def start_requests(self):
        with open("newsUrlCrawl.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield scrapy.Request(row["url"], self.parse_news)

    def parse_news(self, response):
        item = NewscrawlingItem()

        item["source"] = response.xpath(
            '//*[@id="cSub"]/div[1]/em/a/img/@alt'
        ).extract()[0]
        item["category"] = "정치"
        item["title"] = response.xpath('//*[@id="cSub"]/div[1]/h3/text()').extract()[0]
        item["date"] = response.xpath(
            '/html/head/meta[contains(@property, "og:regDate")]/@content'
        ).extract()[0][:8]
        item["article"] = (
            response.xpath(
                '//*[@id="harmonyContainer"]/section/div[contains(@dmcf-ptype, "general")]/text()'
            ).extract()
            + response.xpath(
                '//*[@id="harmonyContainer"]/section/p[contains(@dmcf-ptype, "general")]/text()'
            ).extract()
        )

        print("*" * 100)
        print(item["title"])
        print(item["date"])

        time.sleep(5)

        yield item

