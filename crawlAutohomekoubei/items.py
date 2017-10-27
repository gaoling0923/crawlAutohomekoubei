# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#抓取失败项
class KoubeiFailedItem(scrapy.Item):
    # name = "koubei url crawler failed"
    url = scrapy.Field()
class KoubeiItem(scrapy.Item):
    # 各项定位
    switcher = {
        '购买车型': 'spec_name',
        '购买地点': 'address',
        '购买时间': 'buy_date',
        '裸车购买价': 'buy_price',
        '空间': 'space',
        '动力': 'power',
        '操控': 'manipulation',
        '油耗': 'fuel',
        '舒适性': 'comfort',
        '外观': 'surface',
        '内饰': 'trim',
        '性价比': 'ratio',
        '购车目的': 'purpose',
    }

    # define the fields for your item here like:
    name = scrapy.Field()

    url = scrapy.Field()
    series_id = scrapy.Field()
    series_name = scrapy.Field()
    spec_id = scrapy.Field()

    spec_name = scrapy.Field()
    address = scrapy.Field()
    buy_date = scrapy.Field()
    buy_price = scrapy.Field()

    #汽车之家八项评分
    space = scrapy.Field()
    power = scrapy.Field()
    manipulation = scrapy.Field()
    fuel = scrapy.Field()
    comfort = scrapy.Field()
    surface = scrapy.Field()
    trim = scrapy.Field()
    ratio = scrapy.Field()  #性价比

    purpose = scrapy.Field()  #购车目的

    title = scrapy.Field()
    date = scrapy.Field()

    content = scrapy.Field()
class koubeiItem(scrapy.Item):
    # # 各项定位
    switcher = {
        '购买车型': 'rzhengchetype',
        '购买地点': 'city',
        '购车经销商': 'jxsname',
        '购买时间': 'buydate',
        '裸车购买价': 'buyprice',
        '油耗':'youhao',
        '油耗目前行驶':'youhaodri',
        '目前行驶':'Driving',
        '空间': 'scorespace',
        '动力': 'scorepower',
        '操控': 'scorecontrol',
        '油耗': 'scoreyouhao',
        '舒适性': 'scoreshushi',
        '外观': 'scoreview',
        '内饰': 'scoreneishi',
        '性价比': 'scorecost',
        '购车目的': 'goumaimudi',
    }
    plauthor = scrapy.Field()
    rzhengchexi = scrapy.Field()
    rzhengchetype = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    jxsname = scrapy.Field()
    buydate = scrapy.Field()
    buyprice = scrapy.Field()
    priceunit = scrapy.Field()
    youhao = scrapy.Field()
    youhaounit = scrapy.Field()
    Driving = scrapy.Field()
    Drivingunit = scrapy.Field()
    scorespace = scrapy.Field()
    scorepower = scrapy.Field()
    scorecontrol = scrapy.Field()
    scoreshushi = scrapy.Field()
    scoreyouhao = scrapy.Field()
    scoreview = scrapy.Field()
    scoreneishi = scrapy.Field()
    scorecost = scrapy.Field()
    comentid = scrapy.Field()
    goumaimudi = scrapy.Field()
    webname = scrapy.Field()
    title = scrapy.Field()
    pscore = scrapy.Field()
    percount = scrapy.Field()
    content = scrapy.Field()
    lookcount = scrapy.Field()
    sunumber = scrapy.Field()
    fromurl = scrapy.Field()
    crawldate = scrapy.Field()

class CrawlautohomekoubeiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
