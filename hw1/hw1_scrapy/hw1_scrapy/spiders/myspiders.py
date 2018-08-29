import scrapy
import datetime
import uuid
import os


def get_urls(filename):
    res = []
    with open(filename, "r") as f:
        for line in f:
            res.append(str(line).replace("\n", ""))
    return res


TOTAL_ARTISTS = 5000
TOTAL_ARTWORKS = 3000


class ArtistSpider(scrapy.Spider):
    name = "artist"
    user_agent = 'Mozilla/5.0'

    def start_requests(self):
        start_urls = get_urls("mandatory_artists.txt")
        seedurl = ['https://americanart.si.edu/art/artists']
        for url in start_urls:
            # self.log("collecting %s" % url)
            yield scrapy.Request(url=url, callback=self.parse1)
    # scrapy.Request(url) can return the GET
        for url in seedurl:
            yield scrapy.Request(url=url, callback=self.parse2)

    def parse1(self, response):
        out = {}
        out["raw_content"] = str(response.body)
        out["url"] = str(response.url)
        out["timestamp_crawl"] = int(datetime.datetime.now().timestamp())
        out["doc_id"] = str(uuid.uuid4())
        yield out

    def parse2(self, response):
        path = "//tr/td[1]/a/@href"
        for url in response.xpath(path).extract():   
            yield scrapy.Request(url="https://americanart.si.edu"+url, callback=self.parse1)  
        page = response.css("li.pager__item.pager__item--next a::attr(href)").extract()
        if page:
            yield scrapy.Request(url="https://americanart.si.edu/art/artists"+page[0], callback=self.parse2)

        # for url in response.xpath(path).extract():
        #     import pdb
        #     pdb.set_trace()
        #     self.log("start crawling %s" % url)

        #     scrapy.Request(url="https://americanart.si.edu"+url, callback=self.parse2)

    # def parse3(self, response):
    #     scrapy.Request(url=response.url, callback=self.parse4)
    #     page = response.css("li.pager__item.pager__item--next a::attr(href)").extract()
    #     if page:
    #         scrapy.Request(url=response.url+page[0], callback=self.parse3)

    # def parse4(self, response):
    #     path = "//td/a/@href"
    #     for url in response.xpath(path).extract():
    #         scrapy.Request(url="https://americanart.si.edu"+url, callback=self.parse1)


class ArtworkSpider(scrapy.Spider):
    name = "artwork"
    user_agent = 'Mozilla/5.0'
    val_count = 0

    def start_requests(self):
        start_urls = get_urls("mandatory_artworks.txt")
        seedurl = ['https://americanart.si.edu/art/browse?classification=All&mediums=All&location=All&on_view=0']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse1)


        for url in seedurl:
            yield scrapy.Request(url=url, callback=self.parse2)
    # scrapy.Request(url) can return the GET

    def parse1(self, response):
        out = {}
        out["raw_content"] = str(response.body)
        out["url"] = str(response.url)
        out["timestamp_crawl"] = int(datetime.datetime.now().timestamp())
        out["doc_id"] = str(uuid.uuid4())
        self.val_count += 1
        yield out

    def parse2(self, response):
        # print(response.url)
        # print("反弹"*10)
        # tmp = response.url
        # yield scrapy.Request(url=tmp, callback=self.parse3)
        # print("LGD is champion!") 
        path = "//div/h4/a/@href"
        for url in response.xpath(path).extract():   
            yield scrapy.Request(url="https://americanart.si.edu"+url, callback=self.parse1)     
        page = response.css("li.next a::attr(href)").extract()
        # import pdb
        # pdb.set_trace()
        if page:
            yield scrapy.Request(url='https://americanart.si.edu/art/browse?classification=All&mediums=All&location=All&on_view=0'+"&"+page[0].split("&")[-1], callback=self.parse2)

    # def parse3(self, response):
    #     import pdb
    #     pdb.set_trace()
    #     print(response.url) 
    #     print("shabi"*10)   
    #     path = "//div/h4/a/@href"
    #     for url in response.xpath(path).extract():
    #         yield scrapy.Request(url="https://americanart.si.edu"+url, callback=self.parse1)
