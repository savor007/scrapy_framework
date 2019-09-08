import importlib


# from scrapy_framework.config.settings import SPIDERS
#
#
# for data in SPIDERS:
#     print(data)
#     path=data.rsplit(".",1)[0]
#     cls_name=data.rsplit(".",1)[1]
#     module=importlib.import_module(path)
#     cls=getattr(module, cls_name)
#     print(cls)


d = {'a':1,'b':4,'c':2}
c=sorted(d.items(), key=lambda x: x[1], reverse=False)
print(c)