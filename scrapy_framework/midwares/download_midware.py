from scrapy_framework.html.request import Request
from scrapy_framework.html.response import Response

import random


def get_ua():
    first_num=random.randint(55,69)
    third_num=random.randint(0,3200)
    forth_num=random.randint(0, 140)

    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, forth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return ua


class DownloadMidware(object):
    def process_request(self, request):
        if request.headers==None:
            request.headers=dict()
        request.headers["User-Agent"]=get_ua()
        return request


    def process_response(self, response):
        return response