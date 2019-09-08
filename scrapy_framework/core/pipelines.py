from pprint import pprint


class Scrapy_Pipelines:
    def Pipeline(self, item):
        pprint(item.data)
        return item