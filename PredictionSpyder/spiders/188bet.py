
import scrapy
from scrapy_splash import SplashRequest
from .methods import get_oneeighteight
import time
import json


class OneEightEightSpider(scrapy.Spider):
    name = "188spider"

    start_urls = ["https://www.188bet.com/vi-vn/world-cup#06" + str(i) for i in range(14, 30)]
    # start_urls = ["https://www.188bet.com/vi-vn/world-cup#0614"]

    f = open("188.json", 'w').close()

    script = """
                function main(splash)
                  assert(splash:go(splash.args.url))

                  -- requires Splash 2.3  
                  while not splash:select('.bet-types-table') do
                    splash:wait(0.1)
                  end
                  return {html=splash:html()}
                end
        """

    def start_requests(self):
        for url in self.start_urls:
            time.sleep(10)
            yield SplashRequest(url, self.parse,
                    endpoint='execute',
                    args={
                        'lua_source': self.script
                    },
                    meta={'match_name': url}
                )

    def parse(self, response):
        raw_data_list = get_oneeighteight(response.text, response.meta['match_name'])
        result = []

        # Country name dictionary
        with open('countries_names.json') as countries_name:
            countries_name_dict = json.load(countries_name)

        # parse raw data
        matches_data = [raw_data_list[i:i+3] for i in range(0, len(raw_data_list), 3)]

        for match_data in matches_data:
            team1_data = match_data[0]
            team2_data = match_data[1]
            draw_data = match_data[2]

            match_data_json = {}
            match_data_json['MATCHNAME'] = {}
            if team1_data[0].strip().title() in countries_name_dict:
                match_data_json['MATCHNAME']['team1'] = countries_name_dict[team1_data[0].strip().title()]
            else:
                match_data_json['MATCHNAME']['team1'] = team1_data[0].strip().title()

            if team2_data[0].strip().title() in countries_name_dict:
                match_data_json['MATCHNAME']['team2'] = countries_name_dict[team2_data[0].strip().title()]
            else:
                match_data_json['MATCHNAME']['team2'] = team2_data[0].strip().title()

            match_data_json['CATRAN-onextwo'] = {}
            match_data_json['CATRAN-onextwo']['team1'] = [team1_data[1]]
            match_data_json['CATRAN-onextwo']['team2'] = [team2_data[1]]
            match_data_json['CATRAN-onextwo']['draw'] = [draw_data[1]]

            match_data_json['CATRAN-handicap'] = {}
            match_data_json['CATRAN-handicap']['team1'] = [team1_data[2].split()[0], team1_data[2].split()[1]]
            match_data_json['CATRAN-handicap']['team2'] = [team2_data[2].split()[0], team2_data[2].split()[1]]

            match_data_json['CATRAN-underover'] = {}
            match_data_json['CATRAN-underover']['team1'] = [' '.join(team1_data[3].split()[:2]), team1_data[3].split()[2]]
            match_data_json['CATRAN-underover']['team2'] = [' '.join(team2_data[3].split()[:2]), team2_data[3].split()[2]]

            match_data_json['HIEP1-onextwo'] = {}
            match_data_json['HIEP1-onextwo']['team1'] = [team1_data[1 + 3]]
            match_data_json['HIEP1-onextwo']['team2'] = [team2_data[1 + 3]]
            match_data_json['HIEP1-onextwo']['draw'] = [draw_data[2]]

            match_data_json['HIEP1-handicap'] = {}
            match_data_json['HIEP1-handicap']['team1'] = [team1_data[2 + 3].split()[0], team1_data[2 + 3].split()[1]]
            match_data_json['HIEP1-handicap']['team2'] = [team2_data[2 + 3].split()[0], team2_data[2 + 3].split()[1]]

            match_data_json['HIEP1-underover'] = {}
            match_data_json['HIEP1-underover']['team1'] = [' '.join(team1_data[3 + 3].split()[:2]), team1_data[3 + 3].split()[2]]
            match_data_json['HIEP1-underover']['team2'] = [' '.join(team2_data[3 + 3].split()[:2]), team2_data[3 + 3].split()[2]]

            match_data_json['DATETIME'] = 'Undefined'

            result.append(match_data_json)

        print(result)
        return result






