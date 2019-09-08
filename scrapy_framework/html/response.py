import re
import json
from lxml import etree


class Response(object):
    def __init__(self, url, headers, body, status_code, meta=None):
        self.url = url
        self.headers = headers
        self.body = body
        self.status_code = status_code
        self.meta = meta

    def xpath(self, rule):
        """
        provide xppath method for response
        :param rule:
        :return:
        """

        html = etree.HTML(self.body)
        return html.xpath(rule)

    @property
    def json(self):
        """
        provide json parsing method, for json method string
        :return:
        """
        return json.loads(self.body)

    def re_findall(self, rule, data=None):
        if data is None:
            data = self.body
        return re.findall(rule, data)
