# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Loupan(scrapy.Item):
    mingzi = scrapy.Field()
    link = scrapy.Field()
    loupanzhuangtai = scrapy.Field()

    danjia = scrapy.Field()
    leixing = scrapy.Field()
    quyu = scrapy.Field()
    ziquyu = scrapy.Field()
    dizhi = scrapy.Field()
    dianhua = scrapy.Field()
    kaipan = scrapy.Field()
    jiaofu = scrapy.Field()

    huxing = scrapy.Field()
    mianji = scrapy.Field()
    huxingzhuangtai = scrapy.Field()
    zongjia = scrapy.Field()
    shoufu = scrapy.Field()
    yuegong = scrapy.Field()
