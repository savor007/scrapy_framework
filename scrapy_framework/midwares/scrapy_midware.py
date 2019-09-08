from .download_midware import get_ua

class ScrapyMidware(object):
    def process_request(self, request):
        if request.headers==None:
            request.headers=dict()
        request.headers["User-Agent"]=get_ua()
        return request

    def process_response(self, response):
        return response