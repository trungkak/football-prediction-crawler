
import scrapy
from .methods import get_bet_odds, get_bet_ratio
from scrapy_splash import SplashRequest
import json


class OddsSpider(scrapy.Spider):
    name = "oddsspider"

    start_urls = [
        '/football/world-cup/russia-v-saudi-arabia/winner',
        '/football/world-cup/egypt-v-uruguay/winner',
        '/football/world-cup/morocco-v-iran/winner',
        '/football/world-cup/portugal-v-spain/winner',
        '/football/world-cup/france-v-australia/winner',
        '/football/world-cup/argentina-v-iceland/winner',
        '/football/world-cup/peru-v-denmark/winner',
        '/football/world-cup/croatia-v-nigeria/winner',
        '/football/world-cup/costa-rica-v-serbia/winner',
        '/football/world-cup/germany-v-mexico/winner',
        '/football/world-cup/brazil-v-switzerland/winner',
        '/football/world-cup/sweden-v-south-korea/winner',
        '/football/world-cup/belgium-v-panama/winner',
        '/football/world-cup/tunisia-v-england/winner',
        '/football/world-cup/poland-v-senegal/winner',
        '/football/world-cup/colombia-v-japan/winner',
        '/football/world-cup/russia-v-egypt/winner',
        '/football/world-cup/portugal-v-morocco/winner',
        '/football/world-cup/uruguay-v-saudi-arabia/winner',
        '/football/world-cup/iran-v-spain/winner',
        '/football/world-cup/france-v-peru/winner',
        '/football/world-cup/denmark-v-australia/winner',
        '/football/world-cup/argentina-v-croatia/winner',
        '/football/world-cup/brazil-v-costa-rica/winner',
        '/football/world-cup/nigeria-v-iceland/winner',
        '/football/world-cup/serbia-v-switzerland/winner',
        '/football/world-cup/belgium-v-tunisia/winner',
        '/football/world-cup/germany-v-sweden/winner',
        '/football/world-cup/south-korea-v-mexico/winner',
        '/football/world-cup/england-v-panama/winner',
        '/football/world-cup/japan-v-senegal/winner',
        '/football/world-cup/poland-v-colombia/winner',
        '/football/world-cup/saudi-arabia-v-egypt/winner',
        '/football/world-cup/uruguay-v-russia/winner',
        '/football/world-cup/iran-v-portugal/winner',
        '/football/world-cup/spain-v-morocco/winner',
        '/football/world-cup/australia-v-peru/winner',
        '/football/world-cup/denmark-v-france/winner',
        '/football/world-cup/iceland-v-croatia/winner',
        '/football/world-cup/nigeria-v-argentina/winner',
        '/football/world-cup/mexico-v-sweden/winner',
        '/football/world-cup/south-korea-v-germany/winner',
        '/football/world-cup/serbia-v-brazil/winner',
        '/football/world-cup/switzerland-v-costa-rica/winner',
        '/football/world-cup/japan-v-poland/winner',
        '/football/world-cup/senegal-v-colombia/winner',
        '/football/world-cup/england-v-belgium/winner',
        '/football/world-cup/panama-v-tunisia/winner',
    ]

    start_urls = ['https://www.oddschecker.com' + url for url in start_urls]

    script = """
                function main(splash)
                  assert(splash:go(splash.args.url))

                  -- requires Splash 2.3    
                  while not splash:select('.highcharts-legend') do
                    splash:wait(0.1)
                  end
                  return {html=splash:html()}
                end
        """

    def start_requests(self):
        for url in self.start_urls:
            # yield scrapy.Request(url=url, callback=self.parse)
            yield SplashRequest(url, self.parse,
                endpoint='execute',
                args={
                    'lua_source': self.script
                },
            )

    def parse(self, response):
        odds_json = get_bet_odds(response.text, response.url)
        odds_json[response.url]['ratios'] = get_bet_ratio(response.text)
        return odds_json
