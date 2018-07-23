
import scrapy
from scrapy_splash import SplashRequest
from .methods import get_oneeighteight
import time
import json

from scrapy.selector import Selector



class AmazonSpider(scrapy.Spider):
    name = "amazon"

    start_urls = ["https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Damazon-devices&field-keywords=dress"]
    
    script = """
                function main(splash)
                  assert(splash:go(splash.args.url))

                  -- requires Splash 2.3  
                  while not splash:select('.sx-zero-spacing') do
                    splash:wait(0.1)
                  end
                  return {html=splash:html()}
                end
        """

    def start_requests(self):
        for url in self.start_urls:
            time.sleep(5)
            yield SplashRequest(url, self.parse,
                    endpoint='execute',
                    args={
                        'lua_source': self.script
                    },
                    meta={'match_name': url}
                )

    def parse(self, response):

        # extract and print out image urls
        img_urls = response.xpath('//*[@id="result_1"]/div/div[2]/div/div/a/img').extract()
        
        for img_url in img_urls:
            print(img_urls)

