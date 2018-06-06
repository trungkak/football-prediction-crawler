
import scrapy
from scrapy_splash import SplashRequest
from .methods import get_google_winner
import json


class GoogleWinnerSpider(scrapy.Spider):
    name = 'winnerspider'

    matches = {
        'russia-v-saudi-arabia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11hcjt317s;2;/m/030q7;dt;fp;1',
        'egypt-v-uruguay': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11ggb34yxg;2;/m/030q7;dt;fp;1',
        'morocco-v-iran': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11ggb35h86;2;/m/030q7;dt;fp;1',
        'portugal-v-spain': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdw869;2;/m/030q7;dt;fp;1',
        'france-v-australia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11hcjt2vmy;2;/m/030q7;dt;fp;1',
        'argentina-v-iceland': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11hcjt1vkz;2;/m/030q7;dt;fp;1',
        'peru-v-denmark': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdwwxc;2;/m/030q7;dt;fp;1',
        'croatia-v-nigeria': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdwkfv;2;/m/030q7;dt;fp;1',
        'costa-rica-v-serbia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11hcjt3dsw;2;/m/030q7;dt;fp;1',
        'germany-v-mexico': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11hcjt3cf0;2;/m/030q7;dt;fp;1',
        'brazil-v-switzerland': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11ggb359zf;2;/m/030q7;dt;fp;1',
        'sweden-v-south-korea': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11ggb361_w;2;/m/030q7;dt;fp;1',
        'belgium-v-panama': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdx1m0;2;/m/030q7;dt;fp;1',
        'tunisia-v-england': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11hcjt3znf;2;/m/030q7;dt;fp;1',
        'poland-v-senegal': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdw6t5;2;/m/030q7;dt;fp;1',
        'colombia-v-japan': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11ggb34l7j;2;/m/030q7;dt;fp;1',
        'russia-v-egypt': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11ggb35nz7;2;/m/030q7;dt;fp;1',
        'portugal-v-morocco': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11ggb35wnq;2;/m/030q7;dt;fp;1',
        'uruguay-v-saudi-arabia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdxbrf;2;/m/030q7;dt;fp;1',
        'iran-v-spain': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdw60b;2;/m/030q7;dt;fp;1',
        'france-v-peru': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11hcjt2sjc;2;/m/030q7;dt;fp;1',
        'denmark-v-australia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11ggb35rz5;2;/m/030q7;dt;fp;1',
        'argentina-v-croatia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11hcjt2b7w;2;/m/030q7;dt;fp;1',
        'brazil-v-costa-rica': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdx7vy;2;/m/030q7;dt;fp;1',
        'nigeria-v-iceland': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdw3fg;2;/m/030q7;dt;fp;1',
        'serbia-v-switzerland': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11ggb35w6w;2;/m/030q7;dt;fp;1',
        'belgium-v-tunisia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11ggb35rz3;2;/m/030q7;dt;fp;1',
        'germany-v-sweden': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdwgr3;2;/m/030q7;dt;fp;1',
        'south-korea-v-mexico': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11ggb35qpd;2;/m/030q7;dt;fp;1',
        'england-v-panama': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11ggb356pk;2;/m/030q7;dt;fp;1',
        'japan-v-senegal': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qd_7gl;2;/m/030q7;dt;fp;1',
        'poland-v-colombia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdwkfj;2;/m/030q7;dt;fp;1',
        'saudi-arabia-v-egypt': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdx0vf;2;/m/030q7;dt;fp;1',
        'uruguay-v-russia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11ggb350j3;2;/m/030q7;dt;fp;1',
        'iran-v-portugal': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdwcl0;2;/m/030q7;dt;fp;1',
        'spain-v-morocco': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdx50_;2;/m/030q7;dt;fp;1',
        'australia-v-peru': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdx2wc;2;/m/030q7;dt;fp;1',
        'denmark-v-france': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11hcjt1pz5;2;/m/030q7;dt;fp;1',
        'iceland-v-croatia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdw6tn;2;/m/030q7;dt;fp;1',
        'nigeria-v-argentina': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdv48r;2;/m/030q7;dt;fp;1',
        'mexico-v-sweden': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11ggb35q6f;2;/m/030q7;dt;fp;1',
        'south-korea-v-germany': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11ggb35jf0;2;/m/030q7;dt;fp;1',
        'serbia-v-brazil': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdwvqg;2;/m/030q7;dt;fp;1',
        'switzerland-v-costa-rica': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdvvfs;2;/m/030q7;dt;fp;1',
        'japan-v-poland': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11hcjt1rrx;2;/m/030q7;dt;fp;1',
        'senegal-v-colombia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdwcl2;2;/m/030q7;dt;fp;1',
        'england-v-belgium': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdwt66;2;/m/030q7;dt;fp;1',
        'panama-v-tunisia': 'https://www.google.com.vn/search?q=lich+thi+dau+world+cup+2018&oq=lich&aqs=chrome.1.69i57j69i59j69i60j0l3.1744j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11f4qdx8kb;2;/m/030q7;dt;fp;1'
    }

    script = """
            function main(splash)
              assert(splash:go(splash.args.url))
            
              -- requires Splash 2.3  
              while not splash:select('.liveresults-sports-immersive__lr-imso-ss-wp-ft') do
                splash:wait(0.1)
              end
              return {html=splash:html()}
            end
    """

    # Empty output file
    f = open("winner.json", 'w').close()

    def start_requests(self):
        for match_name, url in self.matches.items():
            # yield scrapy.Request(url=url, callback=self.parse)
            yield SplashRequest(url, self.parse,
                endpoint='execute',
                args={
                    'lua_source': self.script
                },
                meta={'match_name': match_name}
            )

    def parse(self, response):
        winner_json = get_google_winner(response.text, response.meta['match_name'])
        return winner_json
