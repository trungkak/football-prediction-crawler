# football-prediction-crawler

###  Installation

1. Install Scrapy
    ```
    $ pip install scrapy
    ```

2. Install [Docker](https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-16-04)

3. Pull the image
    ```
    $ sudo docker pull scrapinghub/splash
    ```
4. Start the container
    ```
    $ sudo docker run -p 8050:8050 -p 5023:5023 scrapinghub/splash
    ```

5. Splash is now available at 0.0.0.0 at ports 8050 (http) and 5023 (telnet).

### Running

    $ cd PredictionSpyder
    $ scrapy crawl oddsspider -o bet_odds.json -t json
    $ scrapy crawl winnerspider -o winner.json -t json
    $ scarpy crawl keonhacaispider -o keonhacai.json -t json

