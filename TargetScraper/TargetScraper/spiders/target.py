import scrapy


class TargetSpider(scrapy.Spider):
    name = 'target'
    allowed_domains = ['target.com']
    start_urls = ['http://target.com/']

    def parse(self, response):
        pass
