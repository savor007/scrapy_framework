from queue import Queue
import requests
from scrapy_framework.html.response import Response
from scrapy_framework.midwares.download_midware import DownloadMidware
from scrapy_framework.utility.log import logger

class Downloader:
    def get_response(self, request):
        """
        获取request，然后发送request，获取相应response
        :param request:
        :return:
        """
        if request.method.upper() == 'GET':
            response = requests.get(url=request.url, headers=request.headers, params=request.cookies)
        elif request.method.upper() == 'POST':
            response = requests.post(url=request.url, headers=request.headers, data=request.data,
                                     params=request.cookies)

        else:
            raise Exception("The request method {} is not support for this framework.".format(request.method))
            return None
        logger.info("<request url>:{},<response>:{}".format(response.request.url, response.content))
        return Response(url=response.url, body=response.content, headers=response.headers,
                        status_code=response.status_code)
