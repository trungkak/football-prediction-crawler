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

### Crawl data

If you want to crawl winner prediction from google, you need to enable splash to render javascript
    
    $ cd PredictionSpyder
    $ sudo docker run -p 8050:8050 -p 5023:5023 scrapinghub/splash
    $ scrapy crawl winnerspider -o winner.json -t json

==================================================

Or keonhacai prediction

    $ cd PredictionSpyder
    $ scrapy crawl keonhacaispider -o keonhacai.json -t json

==================================================

Or 188 bet prediction, to update ALL MATCHES, run

    $ cd PredictionSpyder
    $ scrapy crawl 188spider -o keonhacai.json -t json

At the time World Cup happens, we could pass a url to crawler
    
    $ cd PredictionSpyder
    $ scrapy crawl 188spider -a default_url='<https://something.com>' -o keonhacai.json -t json


    
### Index database

To update google prediction, run

    python PredictionSpyder/neo4j_import.py --source google --method update
    
To update betodds prediction, run

    python PredictionSpyder/neo4j_import.py --source 188bet --method update
