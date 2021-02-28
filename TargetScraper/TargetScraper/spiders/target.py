import json
import re

import scrapy

API_BASE_URL = "https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1"


class TargetSpider(scrapy.Spider):
    name = "target"
    allowed_domains = ["target.com"]
    start_urls = [
        "https://www.target.com/p/reese-39-s-easter-peanut-butter-eggs-7-2oz-6ct/-/A-53957905"
    ]

    def parse(self, response):
        # scrape params for the API request
        product_url = response.request.url
        # get tcin after the last slash from the URL
        tcin_raw = product_url.split("/")[-1]
        # get the numeric part of tcin
        tcin = tcin_raw.split("-")[1]

        # extract api_key and pricing_store_id from page
        api_key = re.search(r'"apiKey":"(.*?)"', response.text).group(1)
        pricing_store_id = re.search(
            r'"pricing_store_id":"(.*?)"', response.text
        ).group(1)

        # set api params
        params = {
            "key": api_key,
            "tcin": tcin,
            "store_id": "none",
            "has_store_id": "false",
            "pricing_store_id": pricing_store_id,
            "scheduled_delivery_store_id": "none",
            "has_scheduled_delivery_store_id": "false",
            "has_financing_options": "false",
        }
        yield scrapy.FormRequest(
            API_BASE_URL, method="GET", callback=self.parse_api, formdata=params
        )

    def parse_api(self, response):
        pass
