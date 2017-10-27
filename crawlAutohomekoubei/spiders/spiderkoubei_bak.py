# -*- coding: utf-8 -*-
import datetime
import time
import scrapy

import logging

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from crawlAutohomekoubei.items import koubeiItem, KoubeiItem
import sys

logger = logging.getLogger('SpiderkoubeiSpider')


class SpiderkoubeiBakSpider(scrapy.Spider):
    name = 'spiderkoubei_bak'
    allowed_domains = ['k.autohome.com.cn']
    start_urls = ['http://k.autohome.com.cn/4069/'] #注意“/”号有没有分页

    def __init__(self, **kwargs):
        self.count=0

    def start_requests(self):
        # urls = [
        #    'http://k.autohome.com.cn/4069/',
        # ]

        for url in self.start_urls:
            request= scrapy.Request(url=url, callback=self.urlParse)
            request.meta['isjs']='False'
            yield  request

    def urlParse(self, response):
        self.count = self.count + 1
        logger.log(logging.INFO, '页数:%s', self.count)
        totalpage= response.css('.page-item-info::text').extract_first()
        next = response.css('.page-cont  .page  .page-item-next::attr(href)').extract_first()
        nurl = next.strip() if next  else '';
        nextpage = response.urljoin(nurl);
        logger.log(logging.INFO, 'nurl:%s', nurl)
        logger.log(logging.INFO, 'nextpage:%s', nextpage)
        # # 主页名称
        webname = response.css(
            'body  div.content  div.subnav  div.subnav-title  div.subnav-title-name  a::text').extract_first()
        logger.log(logging.INFO, '当前页面名称 %s' % webname)
        #
        # # 标题
        titlet = response.xpath('//*[@id="0"]/dl/dd/ul/li[1]/text()').extract_first()
        pscore = response.xpath('//*[@id="0"]/dl/dd/ul/li[2]/span[1]/span[2]/text()').extract_first()
        percount = response.xpath('//*[@id="0"]/dl/dd/ul/li[2]/span[2]/text()').extract_first()


        soup = BeautifulSoup(response.text, 'lxml')
        titles = soup.findAll('div', class_='cont-title fn-clear')
        for title in titles:
            self._wait()

            url = title.find('a').attrs['href']
            request=scrapy.Request(url='http:' + url, callback=self.parse)
            request.meta['isjs'] = 'True'
            request.meta['webname'] = webname.strip() if webname else ''
            request.meta['title'] = titlet.strip() if titlet else ''
            request.meta['pscore'] = pscore.strip() if pscore else ''
            percount2 = str(percount.strip())
            if percount2:
                pi = percount2.find('人')
                percount3 = percount2[1:pi]
            request.meta['percount'] = percount3 if percount3 else '0'
            yield request
        ##maodian > div > div > div.mouth-cont.js-koubeidataitembox > div.page-cont > div > a.page-item-next
        # next = response.css('.page-cont    a.page-item-next::arrt(href)').extract_first()
        # nurl = next.strip() if next  else '';
        # url = response.urljoin(nurl);
        # print()
        self._wait()
        # yield scrapy.Request(url=nextpage, callback=self.urlParse);
        request = scrapy.Request(url=nextpage, callback=self.urlParse)
        request.meta['isjs'] = 'False'
        yield request
    def parse(self, response):
        # response.
        # #主页名称
        webname = response.css(
            'body  div.content  div.subnav  div.subnav-title  div.subnav-title-name  a::text').extract_first().strip()
        logger.log(logging.INFO, '当前页面名称 %s' % webname)
        #
        #  #标题
        # title= response.xpath('//*[@id="0"]/dl/dd/ul/li[1]/text()').extract_first()
        # pscore= response.xpath('//*[@id="0"]/dl/dd/ul/li[2]/span[1]/span[2]/text()').extract_first()
        # percount= response.xpath('//*[@id="0"]/dl/dd/ul/li[2]/span[2]/text()').extract_first()
        from_url = response.url
        webname = response.meta['webname']
        title = response.meta['title']
        pscore = response.meta['pscore']
        percount = response.meta['percount']
        tcontent = response.meta['tcontent']
        # 块
        # mouthcon=response.css('.mouth')
        # for sub in mouthcon:
        # 评价作者
        # plauthor= response.css('.name-text p a::text').extract_first().strip()
        plauthor = response.css('.user-name a::text').extract_first()
        # print(plauthor)
        # plauthor=''
        # if len(pl)>0:
        #     plauthor =pl[0]
        # 认证车系
        rzhengchexi = response.css(
            'div.mouth-cont  div  div div.mouthcon-cont-left  div  dl:nth-child(1)  dd  a:nth-child(1)::text').extract_first()
        # 认证车型
        # body > div.content > div:nth-child(4) > div > div > div.mouth-cont > div > div > div.mouthcon-cont-left > div > dl:nth-child(1) > dd > a:nth-child(3)
        rzhengchetype = response.css(
            'div.mouth-cont  div  div  div.mouthcon-cont-left  div  dl:nth-child(1)  dd  a:nth-child(3)::text').extract_first()
        # citys = response.css('.choose-dl .c333').extract()
        # print(citys)
        # 购买city
        city = response.css(
            'div.mouth-cont  div  div div.mouthcon-cont-left  div  dl:nth-child(2)  dd::text').extract_first()
        # 购买country
        country = response.css('.choose-dl dd span.js-countryname::text').extract_first()

        # 经销商名称
        jxsname = response.css('.choose-dl .js-dearname::text').extract_first()
        # 购买日期
        # div.mouth-cont > div > div > div.mouthcon-cont-left > div > dl:nth-child(6) > dd > p:nth-child(1)
        buydate = response.css(' div.mouthcon-cont-left div  dl:nth-child(4) dd::text').extract_first()
        # buydate = response.css('div.mouthcon-cont-left div  dl:nth-child(4)  dd p span::text').extract_first().strip()
        # 价格
        buyprice = response.css('div.mouthcon-cont-left div  dl:nth-child(5) dd::text').extract_first()
        priceunit = response.css('div.mouthcon-cont-left div dl:nth-child(5) dd span::text').extract_first()
        # 油耗
        youhao = response.css('div.mouthcon-cont-left div  dl:nth-child(6)  dd  p:nth-child(1)::text').extract_first()
        youhaounit = response.css(
            'div.mouthcon-cont-left div  dl:nth-child(6)  dd  p:nth-child(1) span::text').extract_first()
        # 目前行驶
        Driving = response.css('div.mouthcon-cont-left div  dl:nth-child(6)  dd  p:nth-child(2)::text').extract_first()
        Drivingunit = response.css(
            'div.mouthcon-cont-left div  dl:nth-child(6)  dd  p:nth-child(2) span::text').extract_first()

        # 打分
        scorespace = response.css(
            'div.mouthcon-cont-left  div  dl:nth-child(7)  dd  span.font-arial.c333::text').extract_first()
        scorepower = response.css(
            'div.mouthcon-cont-left div  dl:nth-child(8)    dd  span.font-arial.c333::text').extract_first()
        scorecontrol = response.css(
            'div.mouthcon-cont-left div  dl:nth-child(9)    dd  span.font-arial.c333::text').extract_first()
        scoreshushi = response.css(
            'div.mouthcon-cont-left div  dl:nth-child(10)    dd  span.font-arial.c333::text').extract_first()
        scoreyouhao = response.css(
            'div.mouthcon-cont-left div  dl:nth-child(11)    dd  span.font-arial.c333::text').extract_first()
        scoreview = response.css(
            'div.mouthcon-cont-left div  dl:nth-child(12)    dd  span.font-arial.c333::text').extract_first()
        scoreneishi = response.css(
            'div.mouthcon-cont-left div  dl:nth-child(13)    dd  span.font-arial.c333::text').extract_first()
        scorecost = response.css(
            'div.mouthcon-cont-left div  dl:nth-child(14)    dd  span.font-arial.c333::text').extract_first()
        obje = response.css('div.mouthcon-cont-left div  dl.choose-dl.border-b-no .fn-clear .obje::text').extract()
        sunumber = response.css('.supportNumber::text').extract_first()
        lookcount = response.css(
            ' div.mouthcon-cont-right  div.mouth-remak  div.help  span.fn-left.font-arial.mr-20  span::text').extract_first()

        goumaimudi = ''
        for i in obje:
            goumaimudi = goumaimudi + ' ' + i
        # comenttext = response.css('.text-con *::text').extract()
        # print('comenttext==',comenttext)

        # content = ''
        # for c in comenttext:
        #     if c.strip():
        #         # print(c)
        #         content = content + c

        # comentid = response.css('div.mouthcon-cont-right.commentParentBox div.mouth-main div.mouth-remak  div.allcont.border-b-solid  a.btn.btn-small.fn-left.js-showmessage::attr(data-val)').extract_first()


        logger.log(logging.INFO, 'plauthor %s' % plauthor)
        logger.log(logging.INFO, 'rzhengchexi %s' % rzhengchexi)
        logger.log(logging.INFO, 'rzhengchetype %s' % rzhengchetype)
        logger.log(logging.INFO, 'city %s' % city)
        logger.log(logging.INFO, 'country %s' % country)
        logger.log(logging.INFO, 'jxsname %s' % jxsname)
        logger.log(logging.INFO, 'buydate %s' % buydate)
        logger.log(logging.INFO, 'buyprice %s' % buyprice)
        logger.log(logging.INFO, 'priceunit %s' % priceunit)
        logger.log(logging.INFO, 'youhao %s' % youhao)
        logger.log(logging.INFO, 'youhaounit %s' % youhaounit)
        logger.log(logging.INFO, 'Driving %s' % Driving)
        logger.log(logging.INFO, 'Drivingunit %s' % Drivingunit)
        logger.log(logging.INFO, 'scorespace %s' % scorespace)
        logger.log(logging.INFO, 'scorepower %s' % scorepower)
        logger.log(logging.INFO, 'scorecontrol %s' % scorecontrol)
        logger.log(logging.INFO, 'scoreshushi %s' % scoreshushi)
        logger.log(logging.INFO, 'scoreyouhao %s' % scoreyouhao)
        logger.log(logging.INFO, 'scoreview %s' % scoreview)
        logger.log(logging.INFO, 'scoreneishi %s' % scoreneishi)
        logger.log(logging.INFO, 'scorecost %s' % scorecost)
        # logger.log(logging.INFO, 'comentid %s' % comentid)
        logger.log(logging.INFO, 'goumaimudi %s' % goumaimudi)
        logger.log(logging.INFO, 'tcontent %s' % tcontent)
        logger.log(logging.INFO, 'percount %s' % percount)

        item = koubeiItem()
        item['plauthor'] = plauthor.strip() if plauthor else ''
        item['rzhengchexi'] = rzhengchexi if rzhengchexi else ''
        item['rzhengchetype'] = rzhengchetype if rzhengchetype else ''
        item['city'] = city.strip() if city else ''
        item['country'] = country if country else ''
        item['jxsname'] = jxsname if jxsname else ''
        item['buydate'] = buydate.strip() if buydate else ''
        item['buyprice'] = str(buyprice.strip()) if buyprice else ''
        item['priceunit'] = priceunit.strip() if priceunit else ''
        item['youhao'] = str(youhao) if youhao else ''
        item['youhaounit'] = youhaounit.strip() if youhaounit else ''
        item['Driving'] = str(Driving) if Driving else ''
        item['Drivingunit'] = Drivingunit.strip() if Drivingunit else ''
        item['scorespace'] = str(scorespace) if scorespace else ''
        item['scorepower'] = str(scorepower) if scorepower else ''
        item['scorecontrol'] = str(scorecontrol) if scorecontrol else ''
        item['scoreshushi'] = str(scoreshushi) if scoreshushi else ''
        item['scoreyouhao'] = str(scoreyouhao) if scoreyouhao else ''
        item['scoreview'] = str(scoreview) if scoreview else ''
        item['scoreneishi'] = str(scoreneishi) if scoreneishi else ''
        item['scorecost'] = str(scorecost) if scorecost else ''
        # item['comentid'] = comentid if comentid else ''
        item['goumaimudi'] = goumaimudi if goumaimudi else ''
        item['content'] = tcontent if tcontent else ''
        item['sunumber'] = str(sunumber) if sunumber else ''
        item['lookcount'] = str(lookcount) if lookcount else ''
        #
        # # 主页名称
        item['webname'] = webname
        item['fromurl'] = from_url
        # 标题
        item['title'] = title
        item['pscore'] = str(pscore)
        item['percount'] = str(percount)

        nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['crawldate'] = nowtime
        yield item



        # logger.log(logging.INFO, '当前title %s' % title)

    def parsecoments(self,response):
        print(response.text)

    def _wait(self):
        for i in range(0, 3):
            print('.' * (i%3+1))
            time.sleep(1)

