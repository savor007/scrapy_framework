import importlib
from scrapy_framework.core.downloader import Downloader
from scrapy_framework.core.pipelines import Scrapy_Pipelines
from scrapy_framework.core.scheduler import scheduler
from scrapy_framework.core.scrapy import Spider
from scrapy_framework.html.response import Response
from scrapy_framework.html.request import Request
from scrapy_framework.midwares.download_midware import DownloadMidware
from scrapy_framework.midwares.scrapy_midware import ScrapyMidware
from scrapy_framework.utility.log import logger
from scrapy_framework.config.settings import SPIDERS,PIPELINES,DOWNLOADMIDWARES,SCRAPYMIDWARES


class Engine(object):
    def __init__(self):
        print(SPIDERS)
        print(PIPELINES)
        print(DOWNLOADMIDWARES)
        print(SCRAPYMIDWARES)
        self.downloader = Downloader()
        self.scheduler = scheduler()
        self.download_midware = self._auto_loadsettings(DOWNLOADMIDWARES)
        self.scrapy_midware = self._auto_loadsettings(SCRAPYMIDWARES)
        self.spider = self._auto_loadsettings(SPIDERS, is_Spider=True)
        self.pipelines = self._auto_loadsettings(PIPELINES)
        self.total_response_nums = 0
        self.total_request_nums = 0

    def _process_start_url(self):
        """
        process multiple spider, each spider has list of start urls
        :return:
        """
        for spider_name, spider in self.spider.items():
            for start_request in spider.start_request():  # fetch the request from spider generator
                for scrapy_mid in self.scrapy_midware:
                    start_request = scrapy_mid.process_request(
                        start_request)  # process the request firstly throught the scrapy midware
                start_request.spidername=spider_name     # add corresponding spider name
                self.scheduler.add_request(start_request)  # add the request in the task queue through scheduler
                self.total_request_nums += 1  # increase the total request


    def _process_request_response(self):
        request = self.scheduler.get_request()

        if request is None:
            return
        spider_name=request.spidername
        for download_mid in self.download_midware:
            processed_request = download_mid.process_request(request)

        resp = self.downloader.get_response(processed_request)

        resp.meta=processed_request.meta
        for download_mid in self.download_midware:
            processed_response = download_mid.process_response(resp)

        for scrapy_mid in self.scrapy_midware:
            processed_response = scrapy_mid.process_response(processed_response)

        """
        use dedicate spider here
        """
        spider=self.spider.get(spider_name)

        parsing_method=getattr(spider, processed_request.callback)

        result = parsing_method(processed_response)

        for item in result:
            """
            spider.parse is generator with yield
            """
            if isinstance(item, Request):
                new_request=item
                for scrapy_mid in self.scrapy_midware:
                    new_request = scrapy_mid.process_request(new_request)
                """
                every new request need to add spider name
                """
                new_request.spidername=spider_name   # add spidername for new request
                self.scheduler.add_request(new_request)
                self.total_request_nums += 1

            else:
                for pl in self.pipelines:
                    item=pl.process_item(item, spider)

        self.total_response_nums += 1

    def _start_engine(self):
        """
        1. get start url and format to a Request object
        2. Send the request for start url
        3. Get response of start url
        4. differ the response of start url, if the response is a request, put it into scheduler, else, put it to pipeline
        :return:
        """

        self._process_start_url()  # fetch all of the start urls and put it into scheduler, then to the task queue
        while True:
            self._process_request_response()
            if self.total_request_nums == self.total_response_nums:
                break


    def _auto_loadsettings(self, loadPathSetting, is_Spider=False):
        if is_Spider:
            instance=dict()
            for data in loadPathSetting:
                """
                'Application.DoubanSpider.DoubanSpider', 
                """
                module_path=data.rsplit(".",1)[0]
                cls_name=data.rsplit(".",1)[1]
                module_name=importlib.import_module(module_path)
                cls=getattr(module_name, cls_name)
                instance[cls.name]=cls()

        else:
            instance=list()
            setting_list_sorted=sorted(loadPathSetting.items(), key=lambda x: x[1], reverse=False)
            for module_setting in setting_list_sorted:
                module_path = module_setting[0].rsplit(".", 1)[0]
                cls_name = module_setting[0].rsplit(".", 1)[1]
                module_name = importlib.import_module(module_path)
                cls = getattr(module_name, cls_name)
                instance.append(cls())
        return instance


    def start(self):
        logger.info("start request")
        self._start_engine()
        logger.info("finish all the request")
        logger.info("total request number is %d" % self.total_request_nums)
        logger.info("total response number is %d" % self.total_response_nums)
