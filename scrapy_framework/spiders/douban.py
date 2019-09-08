from scrapy_framework.core.scrapy import Spider
from scrapy_framework.html.request import Request
import urllib
from scrapy_framework.item import Item

from copy import deepcopy


class DoubanSpider(Spider):
    name = "douban"
    start_urls = ["https://movie.douban.com/top250?start=0"]

    def parse(self, response):
        """
        parsing all of movies in the page
        :param Response:
        :return:
        """
        item = dict()
        movie_list = response.xpath(".//ol[@class='grid_view']/li")
        """
        Now, movie_list is a convergence of xpath object. So, it can use the xpath method 
        """

        for movie in movie_list:
            item["title"] = movie.xpath(".//div[@class='hd']/a/span[@class='title']/text()")[0]
            item["description"] = movie.xpath(".//div[@class='bd']/p/text()")[0].strip()
            item["rating"] = movie.xpath(".//div[@class='bd']/div[@class='star']/span[@class='rating_num']/text()")[0]
            item["comment"] = movie.xpath(".//div[@class='bd']/div[@class='star']/span[last()]/text()")[0]
            item["href"] = movie.xpath(".//div[@class='hd']/a/@href")[0]
            if item["href"]:
                new_request = Request(url=item["href"], callback="parse_detail", meta=deepcopy(item))
                # new_request.meta=item
                yield new_request

        next_url = response.xpath(".//div[@class='paginator']/span[@class='next']/a/@href")[0]
        # if next_url:
        #     next_url=urllib.parse.urljoin(response.url, next_url)
        #     yield Request(url=next_url, callback="parse")

    def parse_detail(self, response):
        """

        :param response:
        :return:
        """
        item = response.meta
        item["date"] = response.xpath(".//span[contains(text(), '上映日期')]/following-sibling::span/text()")[0]
        yield Item(data=item)
