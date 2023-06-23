import json
import os
from datetime import datetime

import scrapy
from scrapy.http import TextResponse


class SampleSpider(scrapy.Spider):
    name = "sample_spider"
    base_url = "https://cat-fact.herokuapp.com"
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    custom_settings = {
        "LOG_FILE": f"logs/{name}/{name}_{now}.log",
        "LOG_LEVEL": os.environ.get("LOG_LEVEL", "INFO").upper(),
        "FEEDS": {
            "data/%(name)s/%(name)s_%(now)s.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 4,
                "store_empty": True,
            }
        },
    }

    def start_requests(self):
        url = f"{self.base_url}/facts/random?animal_type=cat&amount=500"
        self.logger.info(f"Scrapping url: {url}")
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response: TextResponse, **kwargs):
        self.logger.info(f"Scrapped data: {response.text}")
        yield from json.loads(response.text)
