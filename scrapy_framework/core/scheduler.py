from queue import Queue

class scheduler(object):
    def __init__(self, max_size=1500):
        self.queue = Queue(maxsize=max_size)

    def add_request(self, request):
        if self.queue.qsize() < self.queue.maxsize:
            self.queue.put(request)
        else:

            # TODO: add customized error handler here from utility

            raise LookupError

    def get_request(self):

        try:
            request= self.queue.get(block=False)
        except Exception as error:
            return None
        else:
            return request



    def _filter_request(self):
        pass
