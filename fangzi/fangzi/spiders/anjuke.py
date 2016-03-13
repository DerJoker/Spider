# -*- coding: utf-8 -*-
import scrapy
import logging
from fangzi.items import Loupan

class AnjukeSpider(scrapy.Spider):
    name = "anjuke"
    allowed_domains = ["anjuke.com"]
    start_urls = (
	"http://nj.fang.anjuke.com/loupan/",
    )

    def parse(self, response):
        for href in response.css('a.next-page.next-link').xpath('./@href'):
            nextpage = response.urljoin(href.extract())
            logging.info(nextpage)
            yield scrapy.Request(nextpage, callback=self.parse)
        for div in response.xpath('//div[@data-link]'):
            link = div.xpath('./@data-link').extract_first()
            mingzi = div.xpath('.//h3/a/text()').extract_first()
            loupanzhuangtai = ';'.join(div.xpath('.//div/i/text()').extract())
            meta = {'mingzi':mingzi, 'link':link, 'loupanzhuangtai':loupanzhuangtai}
            yield scrapy.Request(link, meta=meta, callback=self.parse_loupan)

    def parse_loupan(self, response):
        meta = response.meta

        dd = response.css('dd.price')
        danjia = dd.xpath('./p/em/text()').extract_first()
        leixing = dd.xpath('./p/child::text()').extract_first().strip()

        dizhi = response.css('span.lpAddr-text::text').extract_first().strip()

        p = response.css('p.tel')
        strong = p.xpath('./strong/text()').extract()
        if len(strong) == 2:
            dianhua = ' '.join([strong[0], p.xpath('./em/text()').extract_first(), strong[1]])
        elif len(strong) == 1:
            dianhua = strong[0]
        else:
            dianhua = u'\u6682\u65e0'

        kaipan = response.css('ul.info-left').xpath('./li/span/text()').extract_first()
        jiaofu = response.css('ul.info-right').xpath('./li/span/text()').extract_first()

        meta.update({'danjia':danjia, 'leixing':leixing, 'dizhi':dizhi, 'dianhua':dianhua, 'kaipan':kaipan, 'jiaofu':jiaofu})
        hxzllink = meta['link'].replace('loupan/','loupan/huxing-')
        yield scrapy.Request(hxzllink, meta = meta, callback=self.parse_hxzonglan)

    def parse_hxzonglan(self, response):
        meta = response.meta
        for a in response.css('ul.hx-list').xpath('./li/a'):
            hxlink = a.xpath('./@href').extract_first()
            huxingzhuangtai = a.xpath('./div/div/i/text()').extract_first()
            meta.update({'huxingzhuangtai':huxingzhuangtai})
            yield scrapy.Request(hxlink, meta=meta, callback=self.parse_huxing)

    def parse_huxing(self, response):
        meta = response.meta
        huxing = response.css('div.hx-detail').xpath('./h3/span/text()').extract_first().strip().strip('(').replace(' ', '')
        tmp = {}
        for p in response.css('div.hx-de-right').xpath('./p'):
            strong = p.xpath('./strong/text()').extract_first()
            span = p.xpath('./span/text()').extract_first()
            tmp[strong] = span
        zongjia = tmp.get(u'\u53c2\u8003\u603b\u4ef7:',u'\u65e0')
        shoufu = tmp.get(u'\u53c2\u8003\u9996\u4ed8:',u'\u65e0')
        yuegong = tmp.get(u'\u53c2\u8003\u6708\u4f9b:',u'\u65e0')

        item = Loupan()
        item['mingzi'] = meta['mingzi']
        item['link'] = meta['link']
        item['loupanzhuangtai'] = meta['loupanzhuangtai']
        item['danjia'] = meta['danjia']
        item['leixing'] = meta['leixing']
        dizhi = meta['dizhi'].split(']')
        quyu = dizhi[0].split('-')
        item['quyu'] = quyu[0].split('[')[1].strip()
        item['ziquyu'] = quyu[1].strip()
        item['dizhi'] = dizhi[1].strip()
        item['dianhua'] = meta['dianhua']
        item['kaipan'] = meta['kaipan']
        item['jiaofu'] = meta['jiaofu']
        item['huxingzhuangtai'] = meta['huxingzhuangtai']
        huxing = huxing.split(u'\uff0c')
        item['mianji'] = huxing[2].strip()
        item['huxing'] = ' '.join(huxing[:2])
        item['zongjia'] = zongjia
        item['shoufu'] = shoufu
        item['yuegong'] = yuegong

        yield item
