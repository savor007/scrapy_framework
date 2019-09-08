from .default_config import *
SPIDERS=['spiders.baidu.BaiduSpider','spiders.douban.DoubanSpider']

DOWNLOADMIDWARES={
    'midwares.download_midware.Downloadmidware':2,

}

SCRAPYMIDWARES={
    'midwares.scrapy_midware.Downloadmidware':201,

}


PIPELINES={}

from setting import *

