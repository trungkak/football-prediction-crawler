
import scrapy
from .methods import get_keonhacai
from scrapy_splash import SplashRequest
import json


class KeoNhaCaiSpider(scrapy.Spider):
    name = "keonhacaispider"

    start_urls = ["http://keonhacai.com/ty-le-ca-cuoc-bong-da.html"]

    # Empty output file
    f = open("keonhacai.json", 'w').close()

    def start_requests(self):
        for url in self.start_urls:
            # yield scrapy.Request(url=url, callback=self.parse)
            yield SplashRequest(url, self.parse,
                                endpoint='render.html',
                                )

    def parse(self, response):
        # Change key_term to something like "FIFA WORLD CUP 2018" when it's online
        return get_keonhacai(response.text, key_term="*FIFA WORLD CUP 2018 (IN RUSSIA)")
