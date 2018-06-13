# !/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import pymysql
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import sys

class TrainTicketSpider(object):
    """
    使用Selenium库和PhantomJS浏览器,爬取去哪儿网机票信息
    只实现当日单程票查询
    """

    def __init__(self, depCity, arrCity, depdate):
        self.depCity = depCity
        self.arrCity = arrCity
        self.depDate = depdate
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap["phantomjs.page.settings.userAgent"] = (
        #     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36")
        # self.browser = webdriver.PhantomJS(
        #     executable_path=r"C:\Users\pyin\AppData\Local\Programs\Python\Python36-32\Scripts\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe")
        chrome_options = Options()
        self.browser = webdriver.Chrome("C:\chromedriver\chromedriver.exe", chrome_options=chrome_options)
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='123',
                                          db='test',
                                          port=3306,
                                          charset='utf8',  # 不能用utf-8
                                          cursorclass=pymysql.cursors.DictCursor)

    def crawl(self, url):
        self.browser.set_page_load_timeout(30)
        self.browser.get(url)
        self.browser.save_screenshot('1.png')

        searchType = self.browser.find_elements_by_class_name("input_radio")[0]

        # 始发地
        fromCity = self.browser.find_element_by_id("homeCity")

        # 目的地
        toCity = self.browser.find_element_by_id("destCity")

        # 出发时间
        date = self.browser.find_element_by_id("DDate")

        # 搜索按钮
        searchBtn = self.browser.find_element_by_id("searchBtn")

        aaa = self.browser.find_element_by_id("cui_hd")

        searchType.click()

        fromCity.clear()
        fromCity.send_keys(self.depCity)
        fromCity.click()
        time.sleep(1)

        toCity.clear()
        toCity.send_keys(self.arrCity)
        toCity.click()
        time.sleep(1)

        date.clear()
        date.send_keys(self.depDate)
        date.click()
        time.sleep(1)

        aaa.click()
        searchBtn.click()
        time.sleep(5)
        self.browser.save_screenshot('2.png')

        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(10)
        self.browser.execute_script('window.scrollTo(document.body.scrollHeight, 0)')

        self.parse(current_page=1, date=self.depDate)

    def parse(self, current_page, date):
        html = self.browser.page_source
        HTML = etree.HTML(html)

        # 获取页数
        # pages = HTML.xpath('//a[@class="page"]/text()')
        # page_count = len(pages) + 1

        fly_list = HTML.xpath('//div[@id="flightList"]/div')

        for li in fly_list:
            if li.xpath('.//div[@class="flight-item   "]'):
                li = li.xpath('.//div[@class="flight-item   "]')
                print(len(li))
                for i in li:
                    self.getData(i, date)
            else:
                self.getData(li, date)

        print('爬取结束')
        # 关闭数据库
        self.connection.close()

    def getData(self,li,date):
        # 航空公司/类型
        air_company = li.xpath(
            './/div[@class="flight-row"]/div[@class="flight-col-base"]/div[@class="airline-name"]/text()')[0].strip(
            '\n ')

        air_type = li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-base"]/div[@class="flight-No"]/text()')[
            0]
        fly_info = air_company + air_type
        print('正在获取飞机型号>>>', fly_info)

        # 起飞机场/到达机场/图转机场
        if li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-depart"]/div[@class="flight-detail-airport"]/span/text()'):
            start_station = li.xpath(
                './/div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-depart"]/div[@class="flight-detail-airport"]/text()')[0] + \
                            li.xpath(
                                './/div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-depart"]/div[@class="flight-detail-airport"]/span/text()')[
                                0]
        else:
            start_station = li.xpath(
                './/div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-depart"]/div[@class="flight-detail-airport"]/text()')[0]

        if li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-return"]/div[@class="flight-detail-airport"]/span/text()'):
            end_station = li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-return"]/div[@class="flight-detail-airport"]/text()')[0] + \
                          li.xpath(
                              './/div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-return"]/div[@class="flight-detail-airport"]/span/text()')[0]
        else:
            end_station = li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-return"]/div[@class="flight-detail-airport"]/text()')[0]



        transit_airport_title = ""
        transit_airport_city = ""
        transit_airport = ""
        transit_airport_time = ""
        transit_airport_duration = ""
        if li.xpath(
                './/div[@class="flight-row"]/div[@class="flight-col-more"]/div[@class="flight-stop-info"]/div[@class="flight-stop"]/span[@class="stop-city stop-city-transfer"]/text()'):
            print(len(li.xpath('.//div[@class="trans"]/div[@class="g-up-tips"]/span[@class="t"]/span/text()')))
            transit_airport_city = li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-more"]/div[@class="flight-stop-info"]/div[@class="flight-stop"]/span[@class="stop-city stop-city-transfer"]/text()')[0]

        STATION = (start_station + '-' + end_station).strip('\n ')

        # 起飞时间/到达时间
        start_time = li.xpath(
            './/div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-depart"]/div[@class="flight-detail-time"]/text()')[
            0]
        end_time = li.xpath(
            './/div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-return"]/div[@class="flight-detail-time"]/text()')[
            0]
        TIME = (start_time + '-' + end_time).strip('\n ')

        # 飞行时间
        duration = \
        li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-more"]/div[@class="flight-total-time"]/text()')[
            0].strip('\n ')

        # 参考票价
        price = ""
        # moneyType = li.xpath('.//div[@class="col-price"]/p[@class="prc"]/span[1]/i[1]/text()')[0]
        price = li.xpath(
            './/div[@class="seats-list"]/div[@class="seat-row    "]/div[@class="seat-price"]/div[1]/div[@class="mb5"]/span[2]/text()')[0]
        moneyType = li.xpath(
            './/div[@class="seats-list"]/div[@class="seat-row    "]/div[@class="seat-price"]/div[1]/div[@class="mb5"]/span[2]/dfn/text()')[0]

        # 保存到MySQL数据库
        self.save(air_company, air_type, date, start_time, end_time, duration, start_station,
                  transit_airport_title, transit_airport_city, transit_airport, transit_airport_time,
                  transit_airport_duration, end_station, moneyType, price, "", "xiecheng")

    def save(self, air_company, air_type, dep_date, dep_time, arr_time, duration, dep_airport, transit_airport_title, transit_airport_city,
             transit_airport, transit_airport_time, transit_airport_duration, arr_airport, ticket_price_type, ticket_price, ticket_discount, ticket_resource):
        with self.connection.cursor() as cursor:
            sql = 'INSERT INTO qunaer_flight_info(air_company, air_type, dep_date, dep_time, arr_time, duration, dep_airport, transit_airport_title, transit_airport_city, transit_airport, transit_airport_time, transit_airport_duration, arr_airport, ticket_price_type, ticket_price, ticket_discount, ticket_resource) ' \
                  'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql, (air_company, air_type, dep_date, dep_time, arr_time, duration, dep_airport, transit_airport_title, transit_airport_city, transit_airport,
                                transit_airport_time, transit_airport_duration, arr_airport, ticket_price_type, ticket_price, ticket_discount, ticket_resource))
        self.connection.commit()



if __name__ == '__main__':
    url = 'http://flights.ctrip.com/international/'
    spider = TrainTicketSpider(depCity="上海", arrCity="洛杉矶", depdate="2018-09-28")
    # spider = TrainTicketSpider(depCity=sys.argv[1], arrCity=sys.argv[2], depdate=sys.argv[3])
    spider.crawl(url)