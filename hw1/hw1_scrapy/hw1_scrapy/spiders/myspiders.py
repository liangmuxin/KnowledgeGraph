import scrapy


def get_urls(filename):
    res = []
    with open(filename, "r") as f:
        for line in f:
            res.append(str(line).replace("\n", ""))
    return res


class ArtistSpider(scrapy.Spider):
    name = "artist"

    def start_requests(self):
        start_urls = get_urls("test_artist.txt")
        print(start_urls)
        print("*******************************************")
        urls = ['http://quotes.toscrape.com/page/1/', 'http://quotes.toscrape.com/page/2/']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield response.url
