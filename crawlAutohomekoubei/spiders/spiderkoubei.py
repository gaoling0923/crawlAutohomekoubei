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
class SpiderkoubeiSpider(scrapy.Spider):
    name = 'spiderkoubei'
    allowed_domains = ['k.autohome.com.cn']
    start_urls = [
        # 'http://k.autohome.com.cn/4069/?pvareaid=2099118'
        # 'http://k.autohome.com.cn/4166/?pvareaid=2099118', #宝骏510
        # 'http://k.autohome.com.cn/3824/?pvareaid=2099118', #森雅R7
        # 'http://k.autohome.com.cn/2778/?pvareaid=2099118',#长安CS35
        'http://k.autohome.com.cn/3080/',#瑞风S3
        # 'http://k.autohome.com.cn/spec/27754/view_1764628_1.html?st=7&piap=0|3080|0|0|1|0|0|0|0|0|1'
        # 'http://k.autohome.com.cn/spec/31501/view_1748630_1.html?st=5&piap=0|3080|0|0|1|0|0|0|0|0|1'

                  ] #注意“/”号有没有分页
    base_url = 'http://k.autohome.com.cn'
    def __init__(self, **kwargs):
        self.count=0

    def start_requests(self):
        # urls = [
        #    'http://k.autohome.com.cn/4069/',
        # ]

        for url in self.start_urls:
            request= scrapy.Request(url=url, callback=self.urlParse)
            # request= scrapy.Request(url=url, callback=self.parse)
            request.meta['isjs']='False'
            yield  request

    def urlParse(self, response):
        self.count = self.count + 1
        logger.log(logging.INFO, '页数:%s', self.count)

        # totalpage = response.css('.page-item-info::text').extract_first()
        # next = response.css('.page-cont  .page  .page-item-next::attr(href)').extract_first()
        # nurl = next.strip() if next  else '';
        # nextpage = response.urljoin(nurl);
        # logger.log(logging.INFO, 'nextpage:%s', nextpage)
        #
        # total=response.css(' div.page-cont .page  span.page-item-info::text').extract_first()
        # print('total=',total)

        # if self.count !=1:
        # if self.count >= 20:
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
        # self._wait()
        # yield scrapy.Request(url=nextpage, callback=self.urlParse);
        # request = scrapy.Request(url=nextpage, callback=self.urlParse)
        # request.meta['isjs'] = 'False'
        # yield request

        soup = BeautifulSoup(response.text, 'lxml')
        # 未必有口碑且多页
        page_last = soup.find('a', class_='page-item-last')
        if not page_last:
            return

        url_extend = page_last.attrs['href']
        if url_extend.find('index_') < 0:
            return
        page_number = int(url_extend[url_extend.find('index_') + 6:-14])
        # 页面从2开始到最后
        for num in range(page_number-1):
            self._wait()
            num = str(num+2)
            url = self.base_url + url_extend[0:url_extend.find('index_') + 6] + num + url_extend[url_extend.find('.'):]
            # print("发现链接：%s" % (url))
            logger.log(logging.INFO, 'nextpage:%s', url)
            request = scrapy.Request(url=url, callback=self.urlParse)
            request.meta['isjs'] = 'False'
            yield request
    def parse(self, response):
        from_url = response.url
        webname = response.meta['webname']
        title = response.meta['title']
        pscore = response.meta['pscore']
        percount = response.meta['percount']
        tcontent = response.meta['tcontent']

        # webname = ''
        # title = ''
        # pscore = ''
        # percount = ''
        # tcontent = ''

        sunumber = response.css('.supportNumber::text').extract_first()
        lookcount = response.css(
            ' div.mouthcon-cont-right  div.mouth-remak  div.help  span.fn-left.font-arial.mr-20  span::text').extract_first()


        item = koubeiItem()
        priceunit= '万元'
        youhaounit = '升/百公里'
        Drivingunit = '公里'


        # 评价作者
        # plauthor= response.css('.name-text p a:text').extract_first().strip()
        # plaus = response.css('.user-cont')
        plauthor = response.css('.user-cont a::text').extract_first()
        # 认证车
        rzhengchexi = response.css('#divAuthSpec  .user-car  a::text').extract_first()
        # 认证车型
        # body > div.content > div:nth-child(4) > div > div > div.mouth-cont > div > div > div.mouthcon-cont-left > div > dl:nth-child(1) > dd > a:nth-child(3)
        # rzhengchetype = response.css(
        #     'div.mouth-cont  div  div  div.mouthcon-cont-left  div  dl:nth-child(1)  dd  a:nth-child(3)::text').extract_first()


        soup = BeautifulSoup(response.text, 'lxml')

        # 口碑左侧信息
        mouthcon_cont_left = soup.find('div', class_='mouthcon-cont-left')
        # print('mouthcon_cont_left==',mouthcon_cont_left)
        # item = KoubeiItem()
        # item['url'] = response.url
        #购车目的
        # gmitem = mouthcon_cont_left.find(class_='choose-con').findAll('p', class_='obje')
        # gmtext = ''
        # for g in gmitem:
        #     gmtext=gmtext+g.get_text(strip=True)+' '
        # print('gmtext',gmtext)
        buyprice =''
        youhao=''
        Driving=''
        city=''
        country=''
        for dl_s in mouthcon_cont_left.findAll('dl'):
            item_name = dl_s.find('dt').get_text(strip=True)
            item_value = dl_s.find('dd').get_text(separator=' ', strip=True)
            pitem = dl_s.find('dd').find('p')

            if item.switcher.get(item_name):

                if item_name == '油耗目前行驶':
                    item_value2 = dl_s.find('dd').findAll('p')
                    if len(item_value2) > 1:
                        # print(item_name, item_value2)
                        yh = item_value2[0].get_text(strip=True)
                        youhao = yh[0:yh.find(youhaounit)]
                        # youhao= youhao
                        # item['youhao'] = youhao

                        dv = item_value2[1].get_text(strip=True)
                        Driving = dv[0:dv.find(Drivingunit)]
                        # item['Driving'] = Driving
                elif item_name == '裸车购买价':
                    buyprice = item_value[0:item_value.find(priceunit)].strip()
                    # item['buyprice'] = buyprice
                elif item_name == '购买地点':
                    addrs = item_value.split(' ');
                    if len(addrs)>1:
                        city = addrs[0]
                        # item['city'] = addrs[0]
                        country = addrs[1]
                        # item['country'] = addrs[1]
                else:
                    item[item.switcher.get(item_name)] = item_value
        item['buyprice']=buyprice
        item['youhao']=youhao
        item['Driving']=Driving
        item['city']=city
        item['country']=country
        item['priceunit'] = priceunit
        item['youhaounit'] = youhaounit
        item['Drivingunit'] = Drivingunit
        #
        item['plauthor'] = plauthor.strip() if plauthor else ''
        item['rzhengchexi'] = rzhengchexi if rzhengchexi else ''
        # # 主页名称
        item['webname'] = webname
        item['fromurl'] = from_url
        item['title'] = title
        item['pscore'] = str(pscore)
        item['percount'] = str(percount)
        item['content'] = tcontent
        # 浏览人数
        item['sunumber'] = str(sunumber) if sunumber else ''
        item['lookcount'] = str(lookcount) if lookcount else ''

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














