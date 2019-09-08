from scrapy_framework.core.scrapy import Spider
from scrapy_framework.html.request import Request
import urllib
from scrapy_framework.item import Item

from copy import deepcopy


class BaiduSpider(Spider):
    name = "baidu"
    start_urls = ["https://www.baidu.com", ]
