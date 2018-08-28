import scrapy
import datetime
import uuid


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

    def start_requests(self):
        start_urls = get_urls("test_artist.txt")
        # print(start_urls)
        # print("*******************************************")
        seedurl = ['https://americanart.si.edu/art/artists']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse1)
    # scrapy.Request(url) can return the GET

    def parse1(self, response):
        out = {}
        out["raw_content"] = str(response.body)
        out["url"] = str(response.url)
        out["timestamp_crawl"] = int(datetime.datetime.now().timestamp())
        out["doc_id"] = str(uuid.uuid4())

        return


class ArtworkSpider(scrapy.Spider):
    name = "artwork"

    def start_requests(self):
        start_urls = get_urls("test_artist.txt")
        # print(start_urls)
        # print("*******************************************")
        seedurl = ['https://americanart.si.edu/art/artists']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse1)
    # scrapy.Request(url) can return the GET

    def parse1(self, response):
        out = {}
        out["raw_content"] = str(response.body)
        out["url"] = str(response.url)
        out["timestamp_crawl"] = int(datetime.datetime.now().timestamp())
        out["doc_id"] = str(uuid.uuid4())

        return
