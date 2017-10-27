# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from _md5 import md5

import happybase
import pymongo

from scrapy.conf import settings
import datetime
import random

from crawlAutohomekoubei.items import koubeiItem, KoubeiItem, KoubeiFailedItem



class KoubeiPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        if isinstance(item, KoubeiItem):
            # file = codecs.open('data/koubei/series/%s.jl'%(item['series_name']), 'a', encoding='utf-8')
            with open('data/koubei/series/%s.jl'%(item['series_name']),'a') as file:
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                file.write(line)
            return item
        elif isinstance(item, KoubeiFailedItem):
            with open('data/koubei/failed/koubei_failed_url.jl', 'a') as file:
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                file.write(line)
            return item
        else:
            pass

    def spider_closed(self, spider):
        pass
class randomRowKey(object):
    # 生产唯一key
    def getRowKey(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum

    # print(uniqueNum)
class HBasePipelinef(object):
    def __init__(self):
        host = settings['HBASE_HOST']
        table_name = settings['HBASE_TABLE']
        port = settings['HBASE_PORT']
        self.connection = happybase.Connection(host)
        self.table = self.connection.table(table_name)
        randomrkey=randomRowKey()
        self.rowkey=randomrkey.getRowKey()

    def process_item(self, item, spider):
        # cl = dict(item)

        if isinstance(item, koubeiItem):
            # self.table.put('text', cl)
            print('进入pipline')
            spec_name = item['spec_name']
            address = item['address']
            buy_date = item['buy_date']
            buy_price = item['buy_price']
            space = item['space']
            power = item['power']
            manipulation = item['manipulation']
            fuel = item['fuel']
            comfort = item['comfort']
            surface = item['surface']
            trim = item['trim']
            ratio = item['ratio']
            purpose = item['purpose']
            content = item['content']
            conurl = item['url']
            title = item['title']
            pscore = item['pscore']
            percount = item['percount']
            sunumber = item['sunumber']
            lookcount = item['lookcount']
            crawldate = item['crawldate']

            # self.table.put(md5(conurl.encode('utf-8') + content.encode('utf-8')).hexdigest(), {'cf1:spec_name':spec_name,
            self.table.put(self.rowkey, {'cf1:spec_name':spec_name,
                                        'cf1:address':address,
                                        'cf1:buy_date':buy_date,
                                        'cf1:buy_price':buy_price,
                                        'cf1:space':space,
                                        'cf1:power':power,
                                        'cf1:manipulation':manipulation,
                                        'cf1:fuel':fuel,
                                        'cf1:comfort':comfort,
                                        'cf1:surface':surface,
                                        'cf1:trim':trim,
                                        'cf1:ratio':ratio,
                                        'cf1:purpose': purpose,
                                        'cf1:content': content,
                                         'cf1:conurl': conurl,
                                        'cf1:title': title,
                                        'cf1:pscore': pscore,
                                        'cf1:percount': percount,
                                        'cf1:sunumber': sunumber,
                                        'cf1:lookcount': lookcount,
                                        'cf1:crawldate':crawldate,
                                        })

        return item
class HBasePipeline(object):
    def __init__(self):
        self.host = settings['HBASE_HOST']
        self.table_name = settings['HBASE_TABLE']
        self.port = settings['HBASE_PORT']
        # self.connection = happybase.Connection(host=self.host,port=self.port,, timeout=None, autoconnect=False,timeout=120000,transport='framed' protocol='compact')
        self.connection = happybase.Connection(host=self.host, port=self.port, autoconnect=False)
        # self.connection = happybase.Connection(host=self.host,port=self.port)
        # self.table = self.connection.table(self.table_name)




    def process_item(self, item, spider):
        # cl = dict(item)
        # self.connection = happybase.Connection(host=self.host, port=self.port, timeout=None, autoconnect=False)
        self.connection.open()
        table = self.connection.table(self.table_name)
        if isinstance(item, koubeiItem):
            # self.table.put('text', cl)
            print('进入pipline')
            randomrkey = randomRowKey()
            rowkey = randomrkey.getRowKey()

            plauthor = item['plauthor']
            rzhengchexi = item['rzhengchexi']
            rzhengchetype = item['rzhengchetype']
            city = item['city']
            country = item['country']
            jxsname =item.get('jxsname',' ')
            # jxsname = item['jxsname']
            buydate = item['buydate']
            buyprice = item['buyprice']
            priceunit = item['priceunit']
            youhao = item['youhao']
            youhaounit = item['youhaounit']
            Driving = item['Driving']
            Drivingunit = item['Drivingunit']
            scorespace = item['scorespace']
            scorepower = item['scorepower']
            scorecontrol = item['scorecontrol']
            scoreshushi = item['scoreshushi']
            scoreyouhao = item['scoreyouhao']
            scoreview = item['scoreview']
            scoreneishi = item['scoreneishi']
            scorecost = item['scorecost']
            # comentid = item['comentid']
            goumaimudi = item['goumaimudi']
            webname = item['webname']
            title = item['title']
            pscore = item['pscore']
            percount = item['percount']
            content = item['content']
            sunumber = item['sunumber']
            lookcount = item['lookcount']
            fromurl = item['fromurl']

            crawldate = item['crawldate']
#md5(conurl.encode('utf-8') + content.encode('utf-8')).hexdigest()
            table.put(md5(str(rowkey).encode('utf-8')).hexdigest(), {
                'cf1:plauthor': plauthor,
                'cf1:rzhengchexi': rzhengchexi,
                'cf1:rzhengchetype': rzhengchetype,
                'cf1:city': city,
                'cf1:country':country,
                'cf1:jxsname': jxsname,
                'cf1:buydate': buydate,
                'cf1:buyprice': buyprice,
                'cf1:priceunit': priceunit,
                'cf1:youhao': youhao,
                'cf1:youhaounit': youhaounit,
                'cf1:Driving': Driving,
                'cf1:Drivingunit': Drivingunit,
                'cf1:scorespace': scorespace,
                'cf1:scorepower': scorepower,
                'cf1:scorecontrol': scorecontrol,
                'cf1:scoreshushi': scoreshushi,
                'cf1:scoreyouhao': scoreyouhao,
                'cf1:scoreview': scoreview,
                'cf1:scoreneishi': scoreneishi,
                'cf1:scorecost': scorecost,
                'cf1:goumaimudi': goumaimudi,
                'cf1:webname': webname,
                'cf1:title': title,
                'cf1:pscore': pscore,
                'cf1:percount': percount,
                'cf1:content': content,
                'cf1:sunumber': sunumber,
                'cf1:lookcount': lookcount,
                'cf1:fromurl': fromurl,
                'cf1:crawldate': crawldate
            })
        self.connection.close()
        return item

    # def close_spider(self,spider):
    #     self.connection.close()

        # self.table


class MongoDBPipeline(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        dic = dict(item)
        self.post.insert(dic)
        return item
class CrawlautohomekoubeiPipeline(object):
    def process_item(self, item, spider):
        return item
