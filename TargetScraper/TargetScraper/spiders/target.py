import html
import json
import re

import scrapy

from ..items import ProductItem

API_BASE_URL = "https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1"


class TargetSpider(scrapy.Spider):
    name = "target"
    allowed_domains = ["target.com"]
    start_urls = [
        "https://www.target.com/p/reese-39-s-easter-peanut-butter-eggs-7-2oz-6ct/-/A-53957905"
    ]

    def parse(self, response):
        # scrape params for API request
        # get the URL of current page
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
            API_BASE_URL, method="GET", callback=self.parse_json_data, formdata=params
        )

    def parse_json_data(self, response):
        # Convert all named and numeric character references
        # in the response to the corresponding Unicode characters
        response_text = html.unescape(response.text)

        full_data = json.loads(response_text)
        product_data = full_data["data"]["product"]
        # load the data into item
        item = ProductItem()
        item["title"] = product_data["item"]["product_description"]["title"]
        item["description"] = product_data["item"]["product_description"][
            "downstream_description"
        ]
        item["price"] = product_data["price"]["current_retail"]
        item["image_urls"] = None
        yield item
