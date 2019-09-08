from scrapy_framework.item import Item
from scrapy_framework.html.request import Request
from scrapy_framework.html.response import Response


class Spider:
    def __init__(self):
        start_urls=[]


    def start_request(self):
        for url in self.start_urls:
            yield Request(url=url)


    def parse(self, Response):
        yield Item(Response.body)
