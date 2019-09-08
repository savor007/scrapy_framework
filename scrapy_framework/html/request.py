class Request(object):
    """
    create a instance of Request
    """

    def __init__(self, url, method="GET", headers=None, cookies=None, data=None, callback='parse', meta=None):
        self.url = url
        self.method = method
        self.headers = headers
        self.cookies = cookies
        self.data = data
        self.callback=callback
        self.meta=meta
        self.spidername=""