
import scrapy
from .methods import get_keo_nha_cai
import json


class KeoNhaCaiSpider(scrapy.Spider):
    name = "keonhacaispider"

    start_urls = ["http://keonhacai.com/ty-le-ca-cuoc-bong-da.html"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        return get_keo_nha_cai(response.text)
